"""
该代码主要提取gem5模拟结果中关于指令的hit数和miss数。
gem5的flag信息如下：
    --debug-flags=TLB,PageTableWalker,MMU --debug-flags=Cache --debug-flags=Exec --debug-flags=CacheRepl
"""
import re
import os
import argparse
import matplotlib.pyplot as plt
import numpy as np

def my_args():
    """
    自定义运行此脚本传入的参数
    """
    parser = argparse.ArgumentParser(description='Extract debugging information from gem5')
    parser.add_argument("--cacheline_size", default="0x3f", type=str, nargs ='?',
                        help=f"The size of cacheline. default 64B")
    parser.add_argument("--binary", type=str,
                        help=f"The path of the exec file")
    parser.add_argument("--outputfile_path", type=str, default='m5out', nargs ='?',
                        help=("Output file directory, default: m5out"))
    parser.add_argument("--visualfile_dir", type=str, default='visual', nargs ='?',
                        help=("Visual results output directory"))
    options = parser.parse_args()
    return options


def delete_other(data):
    """
    删除不需要的信息
    """
    out = []
    for line in data:
        if 'system.l2cache' in line or 'system.cpu.dcache' in line:
            continue
        elif ('sendMSHRQueuePacket' in line or 'createMissPacket' in line or 'handleTimingReqMiss' in line
              or 'recvTimingResp' in line or 'sendWriteQueuePacket' in line):
            continue
        elif ('Translating vaddr' in line or 'In protected mode' in line or 'Paging enabled' in line or
              'Handling a TLB' in line or ('Mapping' in line and 'to' in line) or 'Miss was serviced' in line or
              'Entry found with paddr' in line or 'Invalidating' in line or 'dtb' in line):
            continue
        else:
            out.append(line)
    return out


def delete_inst_(data):
    # 删除所有的指令改写部分
    out = []  # 最后的输出数据
    for line in data:
        if 'system.cpu: T0 :' in line:
            # 说明该行是指令
            # 通过判断该行中是否有大写字母，判断该行是否为gem5模拟的指令
            temp = line.split(':')[4].strip()  # 指令部分mov	MOV_R_I
            # 首先看有没有加号，有的话则判断.在不在+后面的字符串中；没有则判断.在不在字符串中
            temp_1 = line.split(':')[3].strip()  # 0x401abc @get_common_indices.constprop.0+12. 0
            if '+' in temp_1:
                temp_2 = temp_1.split('+')[1]
                if temp.isupper() and '.' in temp_2:
                    continue
                else:
                    out.append(line)
            else:
                if temp.isupper() and '.' in temp_1:
                    continue
                else:
                    out.append(line)
        else:
            out.append(line)
    return out

class Gem5DebugMess:
    def __init__(self, read_path, size, output_path, visualfile_path):
        self.path = read_path  # gem5的debug文件路径
        self.icache_line_size = size if size else '0x3f'  # 设置默认值0x3f
        self.write_path = os.path.abspath(output_path)  # 设置输出目录路径
        self.data = []  # 保存初始的debug信息
        self.delete_list = []  # 删除列表中部分项后的列表
        self.sort_list = []  # 按照时钟周期排序后的列表
        self.instruction = {}  # 保存指令的字典:key为指令  value为对应的地址值
        self.icache_cacheline = {}  # 保存cacheline的信息，包括命中与未命中次数
        self.pattern = r'\[([0-9a-fA-F]+):([0-9a-fA-F]+)\]'  # 使用正则表达式匹配 类似[25280:252bf] 的模式
        self.address_pattern = r"0x[0-9a-fA-F]+"
        self.func = {}  # 按照函数名对指令进行排序后的信息
        self.visual_path = visualfile_path if visualfile_path else 'function_inst'
        self.add = r"Block addr\s+0x([0-9a-fA-F]+)\s+\(ns\)\s+moving\s+from\s+to\s+state:"
        self.inst_total = {}  # 统计详细信息

    def process(self):
        """整个代码的运行控制函数"""
        # 从debug调试信息文件中读取数据
        self.read_from_debug()
        # # 使用 lambda 函数提取冒号前面的数字作为排序的关键字，进行排序
        self.sort_list = sorted(self.data, key=lambda x: int(x.split(':')[0]))
        # 删除其他不需要的信息
        self.delete_list = delete_other(self.sort_list)
        # 删除关于指令扩写的部分
        self.delete_list = delete_inst_(self.delete_list)
        self.deal_inst(self.delete_list, self.icache_line_size)
        self.total = self.is_show_terminal(self.instruction)
        self.func = self.separation_function(self.instruction)
        self.func_hit_miss = self.count_func_miss_hit(self.func)
        
        # 写信息到文件中
        self.write_to_file(self.func, 'func.txt')
        self.write_to_file(self.inst_total, 'inst.txt')
        self.write_to_file(self.icache_cacheline, 'cacheline.txt')
        self.write_to_file(self.func_hit_miss, 'func_miss_hit.txt')

        # 可视化
        self.visual(self.func, self.visual_path)
        # self.visual_portrait(self.func_hit_miss, self.visual_path)
        

    def deal_inst_toal(self, data_1, data_2):
        out = {}
        for keys, values in data_1.items():
            out[keys] = values
        for keys, values in data_2.items():
            out[keys] = values
        return out
        

    def count_func_miss_hit(self, data):
        # 计算每个函数的指令的hit和miss数
        out = {}
        for keys, values in data.items():
            miss_hit = []
            miss = 0
            hit = 0
            for value in values:
                miss += value[1]
                hit += value[2]
            miss_hit.append(miss)
            miss_hit.append(hit)
            out[keys] = miss_hit
        return out

    # 判断是否在终端显示最后的结果
    def is_show_terminal(self, data):
        out = {}
        miss_total = 0
        hit_total = 0
        for keys, values in self.instruction.items():
            # values = ['', '', 0, 0]
            miss = int(values[2])
            hit = int(values[3])
            miss_total += miss
            hit_total += hit
        out['Total miss number: '] = miss_total
        out['Total hit number: '] = hit_total
        miss_rate = miss_total/(miss_total+hit_total)
        hit_rate = hit_total/(miss_total+hit_total)
        miss_rate_percentage = "{:.5%}".format(miss_rate)
        hit_rate_percentage = "{:.5%}".format(hit_rate)
        out['Miss rate: '] = miss_rate_percentage
        out['Hit rate: '] = hit_rate_percentage
        return out 
        
    def separation_function(self, data):
        # 可视化所有函数
        func = {}  # 保存所有函数中对应的
        for keys, values in data.items():
            # keys = inst: 0x4014c0 @_start:  hint:
            # keys = 0x4014c0 @_start:  hint:
            # values = ['[14c0:14ff]', '0x4014c0 -> 0x14c0', 1, 0]
            if '_end' not in keys:
                key_func = keys.split('@')[1].split(':', 1)[0].strip().split('+')[0]  # _start
                if key_func not in func.keys():
                    func[key_func] = []
                keys_address = keys.split('@')[0].strip()  # 0x4014c0
                keys_inst = keys.split(':', 2)[1].strip()  #  hint
                func_1 = keys_address + '@' + keys_inst
                func_value = [func_1, values[2], values[3]]
                func[key_func].append(func_value)
        return func
    
    def visual(self, data, output_dir):
        """
        data: 一个字典，键为函数名，值为包含指令及其对应的miss和hit数量的列表
        output_dir: 图片保存的文件夹路径
        """
        # 创建保存图片的文件夹
        if not isinstance(output_dir, str):
            raise TypeError("output_dir must be a string")
        output = os.path.join(self.write_path, output_dir)
        os.makedirs(output, exist_ok=True)
        
        # 遍历每个函数的数据
        for func_name, inst_data in data.items():
            # 获取指令、miss数量和hit数量
            instructions = [inst[0] for inst in inst_data]
            misses = [inst[1] for inst in inst_data]
            hits = [inst[2] for inst in inst_data]
            
            # 设置x轴标签和柱状图的位置
            x = np.arange(len(instructions))
            
            # 动态调整图的大小，增加图的高度以增大y轴标签之间的间距
            fig, ax = plt.subplots(figsize=(max(len(instructions) * 0.3, 15), 8))
            
            # 绘制柱状图
            bar_width = 0.35
            bars_miss = ax.bar(x - bar_width/2, misses, bar_width, label='Miss')
            bars_hit = ax.bar(x + bar_width/2, hits, bar_width, label='Hit')
            
            # 在每个柱子上方显示数值
            for bar in bars_miss:
                height = bar.get_height()
                ax.annotate(f'{height}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

            for bar in bars_hit:
                height = bar.get_height()
                ax.annotate(f'{height}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')
            
            # 设置标签
            ax.set_xlabel('Instructions')
            ax.set_ylabel('Count')
            ax.set_title(func_name)
            ax.set_xticks(x)
            ax.set_xticklabels(instructions, rotation=45, ha='right')  # 旋转x轴标签
            ax.legend()
            
            # 设置y轴标签
            max_count = max(max(misses), max(hits)) + 3
            ax.set_ylim(0, max_count)
            
            # 保存图片
            plt.tight_layout()  # 自动调整布局
            plt.savefig(os.path.join(output, f'{func_name}.png'))
            plt.close()  # 关闭当前图形，以释放内存

    def autolabel_portrait(self, rects, ax):
        """
        Attach a text label above each bar in *rects*, displaying its width.
        """
        for rect in rects:
            width = rect.get_width()
            ax.annotate('{}'.format(width),
                        xy=(width, rect.get_y() + rect.get_height() / 2),
                        xytext=(3, 0),  # 3 points horizontal offset
                        textcoords="offset points",
                        ha='left', va='center')

    # 竖屏显示
    def visual_portrait(self, data, output_dir):
        """
        data：待显示的数据，默认按照字典处理
        output_dir：要保存的可视化的文件路径
        """
        # 创建保存图片的文件夹
        if not isinstance(output_dir, str):
            raise TypeError("output_dir must be a string")
        output = os.path.join(self.write_path, output_dir)
        os.makedirs(output, exist_ok=True)
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

        labels = [keys for keys in data.keys()]  # 保存y轴标签的列表
        data_num_1 = [values[0] for values in data.values()]  # 保存并列的柱状体图中第一列的数据的列表
        data_num_2 = [values[1] for values in data.values()]  # 保存并列的柱状体图中第二列的数据的列表

        num_functions = len(labels)  # 函数的个数
        height = max(0.05, min(0.1, 3 / num_functions))  # 动态计算条形图的高度，限制在0.1到1之间

        # 绘制并列柱状图
        y = np.arange(len(labels))  # 标签位置

        fig, ax = plt.subplots(figsize=(8, num_functions * 0.5))
        rects1 = ax.barh(y - height/2, data_num_1, height, label='miss')
        rects2 = ax.barh(y + height/2, data_num_2, height, label='hit')

        # 为x轴、标题和y轴等添加一些文本
        ax.set_xlabel('num', fontsize=16)
        ax.set_ylabel('func', fontsize=16)
        ax.set_title('func_miss_hit')
        ax.set_yticks(y)  # 设置y轴标签
        ax.set_yticklabels(labels)  # 设置标签
        ax.tick_params(axis='y', labelsize=12)  # 设置y轴标签字体大小为12
        ax.legend()

        # 在rects中的每个条形条上方附加一个文本标签，显示其宽度
        self.autolabel_portrait(rects1, ax)
        self.autolabel_portrait(rects2, ax)

        fig.tight_layout()
        # 保存图片
        plt.tight_layout()  # 自动调整布局
        plt.savefig(os.path.join(output, 'func_hit_miss.png'))
        plt.close()  # 关闭当前图形，以释放内存



    def read_from_debug(self):
        """从debug.txt中读取信息到列表中"""
        with open(self.path, 'r') as f_read:
            for line in f_read.readlines():
                self.data.append(line.strip())

    def write_to_file(self, data, filename):
        """将最后的结果输出到txt文件中"""
        path = os.path.join(self.write_path, filename)
        # 确保目录存在
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f_write:
            for key, value in data.items():
                temp = str(key) + ":   " + str(value) + "\n"
                f_write.write(temp)

    def deal_inst(self, data, size):
        """将指令和地址对应起来"""
        inst = ''  # 指令
        vaddr_to_paddr = []  # 虚拟地址向物理地址转换的信息
        # 初始化
        for line in data:
            # 初始化虚拟地址向物理地址转换的信息
            if 'Translated' in line:
                # 说明此行是虚拟地址向物理地址转换的操作
                temp = line.split(':')[2].strip().split(' ', 1)[1].strip().split('.')[0]  # 0x7ffff8020000 -> 0x26000
                if temp not in vaddr_to_paddr:
                    vaddr_to_paddr.append(temp)
            # 初始化指令
            if 'system.cpu: T0' in line:
                temp = line.split(':', 4)[4].replace('\t', ' ')  # 指令 push	rbp
                temp_1 = line.split(':', 4)[3].strip()  # 0x1198 @main
                inst = temp_1 + ': ' + temp  # 类似于0x1198 @main: push rbp这样的指令格式
                self.instruction[inst] = ['', '', 0, 0]
            # 初始化cacheline的详细信息
            if 'system.cpu.icache: access for ReadReq' in line and 'IF miss' in line:
                match = re.search(self.pattern, line)
                icache_address_ = match.group(0)  # icache_address_ line的范围
                # 这行代码就是为了解决在短周期内，cpu同时访问同一个cacheline的miss情况
                self.icache_cacheline[icache_address_] = ['', '']

        # 详细处理每一行
        for line in data:
            # 判断该cache line在不在cache中
            if 'system.cpu.icache: access for ReadReq' in line and 'IF miss' in line:
                # 说明此时的cache line不在cache中，需要读取这个cache line的地址范围
                match = re.search(self.pattern, line)
                icache_address = match.group(0)  # icache_address就是该cache line的范围
                self.icache_cacheline[icache_address][0] = '0->1'  # cacheline_dict保存的是icache_address，及状态
                icache_cacheline_address_ori = icache_address.split(':')[0].split('[')[1]  # cacheline的首地址 0x25280
                for paddr in vaddr_to_paddr:
                    temp = paddr.split('->')[1].strip()  # 0x7ffff8020000 -> 0x26000  取到0x26000
                    if '0x' in temp:
                        temp_1 = temp.split('0x')[1]  # 从0x26000取到26000
                    if temp_1 == icache_cacheline_address_ori:
                        # 说明当前cacheline已经被映射到物理地址上
                        self.icache_cacheline[icache_address][1] = paddr 
                        break
                continue
            # 表明该cache line即将读入cache中
            if 'system.cpu.icache: Block for addr ' in line and ' being updated in Cache' in line:
                continue
            # 当该cache line被加载到cache中时，该cache line的信息
            if 'system.cpu.icache: Replacement victim: state:' in line:
                continue
            # 判断是否有清除cache的情况出现
            if 'system.cpu.icache: Create CleanEvict CleanEvict' in line:
                # 说明此时出现了清除缓存的情况，需要保存被清除的缓存块
                match_replacement = re.search(self.pattern, line)
                replacement_address = match_replacement.group(0)  # 被替换的地址信息
                if replacement_address in self.icache_cacheline.keys():
                    # 如果被替换cache line的地址范围在cache中，则修改对应的cache line状态为0
                    self.icache_cacheline[replacement_address][0] = '2->0'
                continue
            # 判断缓存块是否已经加载到cache中
            if ('moving from  to state' in line and 'system.cpu.icache:' in line):
                # 说明此时将新的cache line移到cache中
                match_0 = ''
                match_0 = re.search(self.add, line)
                if match_0:
                    addr = match_0.group(1)
                    num1 = int(addr, 16)
                    num2 = int(size, 16)
                    # 执行加法操作
                    result = num1 + num2
                    # 将结果转换回十六进制字符串
                    result_hex = hex(result)[2:]  # 将整数转换为十六进制字符串，并去掉开头的 '0x'
                    icache_loaded_cache = '[' + addr + ':' + result_hex + ']'  # 保存即将被加载到cache中的cache line地址范围
                else:
                    icache_loaded_cache = '[0:3f]'

                self.icache_cacheline[icache_loaded_cache][0] = '1->2'

                continue
            # 判断是不是指令
            if 'system.cpu: T0' in line and '@' in line:
                # 说明此时处理的是指令
                temp = line.split(':', 4)[4].replace('\t', ' ')  # 指令 push	rbp
                temp_1 = line.split(':', 4)[3].strip()  # 0x1198 @main
                current_address = temp_1.split('@')[0].strip().split('0x')[1]  # 当前指令地址1198
                inst = temp_1 + ': ' + temp  # 类似于0x1198 @main: push rbp这样的指令格式
                for keys, values in self.icache_cacheline.items():
                    # 类似这样的keys = [26000:2603f]   values = ['0->1', '0x7fff -> 0x26000']
                    if values[1] == '':
                        continue
                    vaddr = int(values[1].split('->')[0].split('0x')[1], 16)  # 获取虚拟地址并转换为整数
                    vaddr_add_cacheline_size = vaddr + int(self.icache_line_size, 16)  # 执行十六进制加法运算

                    paddr = int(values[1].split('->')[1].split('0x')[1], 16)  # 获取物理地址并转换为整数
                    paddr_add_cacheline_size = paddr + int(self.icache_line_size, 16)  # 执行十六进制加法运算

                    current_address_shi = int(current_address, 16)  # 当前指令的地址转为十六进制整数
                    # 通过映射关系中的虚拟地址加cacheline大小，判断指令地址是否在该范围内
                    if ((vaddr <= current_address_shi <= vaddr_add_cacheline_size) or 
                        (paddr <= current_address_shi <= paddr_add_cacheline_size)):
                        self.instruction[inst][0] = keys
                        self.instruction[inst][1] = values[1]
                        if self.icache_cacheline[keys][0] == '1->2':  # 说明此指令是该cache line中cpu访问的第一条指令
                            # 直接让第一条指令的miss数等于上面IF miss的数量，然后将该值清零
                            self.instruction[inst][2] += 1
                            self.icache_cacheline[keys][0] = '2->2'
                        elif self.icache_cacheline[keys][0] == '2->2':
                            # 说明此指令已经在cache中出现过，当该指令再次出现的时候，Hit数+1
                            self.instruction[inst][3] = self.instruction[inst][3] + 1
                        break  
 
if __name__ == '__main__':
    options = my_args()
    debug = Gem5DebugMess(options.binary, options.cacheline_size, options.outputfile_path, options.visualfile_dir)
    # debug = Gem5DebugMess('./debug_static.txt', '0x3f', './m5out', '1',)
    debug.process()
