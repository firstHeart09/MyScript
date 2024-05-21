#!/bin/bash

# This file is used to determine if the instruction has hit

rm -f instruction_output.txt instruction_sum.txt address.t*

filename="$1"

rm -f "$filename.sorted" "$filename.tmp"

# Generate address mapping file
address_pattern="Translated"
# Use awk delete line
awk -v pattern="$address_pattern" '$0 ~ pattern' "$filename" > "$filename.translated"
echo "$filename.translated is ok!"

awk '{ 
    match($0, /0x[0-9a-fA-F]+ -> 0x[0-9a-fA-F]+/, arr); 
    if (arr[0] != "") 
        print arr[0] 
}' "$filename.translated" > address.tmp_nosort

# 转换十六进制到十进制并排序
awk '
{
    split($1, a, "0x")
    printf "%s %s\n", strtonum("0x"a[2]), $0
}
' address.tmp_nosort | sort -n | awk '
{
    $1 = sprintf("0x%x", $1)
    sub(/^[^ ]+ /, "", $0)
    if (!seen[$0]++) print
}
' > address.tmp

echo "address.tmp is ok"

# Process virtual to physical mmap
#mmap=-1
declare -A addr_mmaps

gawk '
BEGIN {
    prev_diff = -1  # 初始化 prev_diff
}
{
    virtual_addr = strtonum("0x" substr($1, 3))  # 提取和转换虚拟地址
    physical_addr = strtonum("0x" substr($3, 3)) # 提取和转换物理地址
    diff = virtual_addr - physical_addr

    if (prev_diff != diff) {  # 如果当前差值与之前的差值不同
        print $0 >> "address.txt"             # 输出当前行
	#addr_mmaps["0x" virtual_addr] = sprintf("0x%x", diff) # 保存到 addr_mmaps
	#printf "%s: 0x%018x\n", $1, diff >> "addr_mmaps.txt"  # 将键值对保存到文件 addr_mmaps.txt 中
        prev_diff = diff     # 更新前一个差值
    }
}
' address.tmp

echo "虚地址到物理地址的映射已存入文件"
rm -f m5out/debug_info.txt.translated

# Create an associative array in bash to store the key-value pairs
declare -A cache_lines

filter_instructions="system\\.cpu: T0 \\:.*?\\. [0-9]+ \\:"
filter_pattern="system\\.l2cache|system\\.cpu\\.dcache|sendMSHRQueuePacket|createMissPacket|handleTimingReqMiss|recvTimingResp|sendWriteQueuePacket|system\\.cpu\\.mmu\\.dtb|system\\.cpu\\.mmu\\.itb"

# Use awk delete line
awk -v pattern1="$filter_pattern" -v pattern2="$filter_instructions" '$0 !~ pattern1 && $0 !~ pattern2' "$filename" > "$filename.tmp"

# Sort the filtered file by the timestamp
sort -k1,1n "$filename.tmp" > "$filename.sorted"

# Read through the sorted file and process each line
echo "process instruction"
gawk -v addr_file="address.txt" '
BEGIN {
    # 读取 addr_mmaps.txt 文件并存储键值对，保持顺序
    idx = 0
    while ((getline < addr_file) > 0) {
        split($0, kv, "->")
	gsub(/^[ \t]+|[ \t]+$/, "", kv[1])  # 去除键两边的空格
        gsub(/^[ \t]+|[ \t]+$/, "", kv[2])  # 去除值两边的空格
        addr_mmaps[idx] = kv[1]
        addr_values[kv[1]] = kv[2]
        idx++
    }
    close(addr_file)
}
{
    line = $0
    if (match(line, /access for ReadReq \[([0-9a-fA-F:]+)\] IF miss/, m)) {
        key = m[1]
        cache_lines[key] = 0
        next
    }
    #if (match(line, /access for ReadReq \[([0-9a-fA-F:]+)\] IF hit/, m)) {
    #    key = m[1]
    #    cache_lines[key] = 3
    #    echo "lllllllllll"
    #    next
    #}
    if (match(line, /Block addr 0x([0-9a-fA-F]+) \(ns\) moving from/, m)) {
        addr = "0x" m[1]
        for (key in cache_lines) {
            if (index(key, addr) != 0) {
		cache_lines[key] = or(cache_lines[key], 2)
                break
            }
        }
        next
    }
    if (match(line, /Create CleanEvict CleanEvict \[([0-9a-fA-F:]+)\]/, m)) {
        key = m[1]
        delete cache_lines[key]
        next
    }
    if (match(line, /system.cpu: T0 : 0x([0-9a-fA-F]+) @([^[:space:]]+)[[:space:]]*: (.+)/, m)) {
        virtual_addr = "0x" m[1]
        timestamp = m[2]
        instruction = m[3]

        # 计算物理地址
        prev_key = ""
        virtual_addr_dec = strtonum(virtual_addr)
        for (i = 0; i < idx; i++) {
            key = addr_mmaps[i]
            key_dec = strtonum(key)
            if (key_dec > virtual_addr_dec) break
            prev_key = key
        }
        if (prev_key != "") {
            prev_diff_dec = strtonum(addr_values[prev_key])
            physical_addr = virtual_addr_dec - strtonum(prev_key) + prev_diff_dec
            hex_physical_addr = sprintf("0x%x", physical_addr)
            # 处理缓存行
            for (key in cache_lines) {
                split(key, range, ":")
                start_addr = strtonum("0x" range[1])
                end_addr = strtonum("0x" range[2])
		printf "%s %s\n", start_addr, end_addr >> "instruction.txt"
                if (physical_addr >= start_addr && physical_addr <= end_addr) {
		    if (and(cache_lines[key], 1) != 0) {
                        miss = "0"
			hit = "1"
                    } else {
                        miss = "1"
			hit = "0"
			cache_lines[key] = or(cache_lines[key], 1)
                    }
                    printf "%-15s|%-25s|%-45s|[%-12s]|%s|%s\n", virtual_addr, timestamp, instruction, key, miss, hit >> "instruction_output.txt"
                }
            }
        }
    }
}
' "$filename.sorted"

awk -F'|' '
{
    key = $1 "|" $2 "|" $3 "|" $4
    if (!(key in seen)) {
        order[++count] = key
        seen[key] = 1
    }
    sum1[key] += $5
    sum2[key] += $6
    hit += $6
    miss += $5
}
END {
    for (i = 1; i <= count; i++) {
        key = order[i]
        printf "%s|%d|%d\n", key, sum1[key], sum2[key]
    }
    printf "Miss:%d Hit:%d", miss, hit
}
' instruction_output.txt > instruction_sum.txt
echo "finish"

# Clean up tmporary file
rm -f address.tmp address.tmp_nosort "$filename.translated"

