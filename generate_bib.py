#!/usr/bin/env python3
import re
import os
import argparse

def extract_citations(tex_file, verbose=False):
    """从 .tex 文件中提取所有引用键"""
    citations = []
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配 \cite{...} 和 \citep{...} 中的引用，支持同一行多个
    cite_pattern = r'\\cite(?:p)?\{([^}]+)\}'
    matches = re.findall(cite_pattern, content)
    
    for match in matches:
        # 分割多个引用（逗号分隔）并去除每个键的空格
        keys = [key.strip() for key in match.split(',')]
        # 过滤掉空键
        keys = [key for key in keys if key]
        citations.extend(keys)
    
    # 去重但保持顺序
    seen = set()
    ordered_citations = []
    for key in citations:
        if key not in seen:
            seen.add(key)
            ordered_citations.append(key)
            if verbose:
                print(f"Found citation key: {key}")
    
    return ordered_citations

def parse_bib_file(bib_file, verbose=False):
    """解析 .bib 文件，返回字典 {key: entry}，处理嵌套 {}"""
    entries = {}
    current_entry = None
    in_entry = False
    brace_level = 0
    current_field = []
    field_name = None
    
    with open(bib_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('@'):
            # 新条目开始
            match = re.match(r'@(\w+)\{([^,]+),', line)
            if match:
                entry_type = match.group(1)
                key = match.group(2)
                current_entry = {'type': entry_type, 'key': key, 'fields': []}
                in_entry = True
                brace_level = 1  # @type{key, 已经有一个 {
        elif in_entry:
            if line == '}':
                brace_level -= 1
                if brace_level == 0:
                    # 条目结束
                    if current_entry:
                        entries[current_entry['key']] = current_entry
                        if verbose:
                            print(f"Parsed bib entry: {current_entry['key']}")
                    in_entry = False
                    current_entry = None
                    current_field = []
                    field_name = None
            elif '=' in line and brace_level == 1:
                # 新字段开始
                if current_field and field_name:
                    if current_entry is None:
                        raise ValueError("Field found outside of an entry.")
                    current_entry['fields'].append(f"{field_name} = {''.join(current_field)}")
                parts = line.split('=', 1)
                field_name = parts[0].strip()
                value = parts[1].strip()
                current_field = [value]
                # 检查 { 嵌套
                brace_level += value.count('{') - value.count('}')
            else:
                # 字段继续
                current_field.append(' ' + line)
                brace_level += line.count('{') - line.count('}')
        
        i += 1
    
    # 处理最后一个字段
    if current_field and field_name and current_entry and in_entry:
        current_entry['fields'].append(f"{field_name} = {''.join(current_field)}")
    
    return entries

def generate_sorted_bib(tex_file, bib_file, output_file, verbose=False):
    """生成排序后的 .bib 文件"""
    citations = extract_citations(tex_file, verbose=verbose)
    entries = parse_bib_file(bib_file, verbose=verbose)
    
    # 按 tex 中的顺序排序
    sorted_entries = []
    for key in citations:
        if key in entries:
            entry = entries[key]
            # 构建 BibTeX 条目
            bib_entry = f"@{entry['type']}{{{entry['key']},\n"
            bib_entry += '\n'.join(f"  {field}" for field in entry['fields'])
            bib_entry += '\n}\n\n'
            sorted_entries.append(bib_entry)
            if verbose:
                print(f"Adding entry for key: {key}")
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(sorted_entries)
    
    print(f"Generated {output_file} with {len(sorted_entries)} entries.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate sorted BibTeX file from LaTeX citations.")
    parser.add_argument('--tex', default='mainTemplatePDF.tex', help='Input LaTeX file')
    parser.add_argument('--bib', default='refs.bib', help='Input BibTeX file')
    parser.add_argument('--output', default='mainTemplatePDF.bib', help='Output BibTeX file')
    # Allow debug output with "--verbose" option
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output for debugging', default=False)
    
    args = parser.parse_args()
    
    tex_file = args.tex
    bib_file = args.bib
    output_file = args.output
    
    if not os.path.exists(tex_file):
        print(f"Error: {tex_file} not found.")
        exit(1)
    
    if not os.path.exists(bib_file):
        print(f"Error: {bib_file} not found.")
        exit(1)
    
    generate_sorted_bib(tex_file, bib_file, output_file, verbose=args.verbose)
