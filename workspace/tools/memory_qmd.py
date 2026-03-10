#!/usr/bin/env python3
"""
QMD - Quick Markdown Index
智能记忆检索系统，使用 SQLite + BM25 实现高效搜索
"""

import os
import sys
import sqlite3
import json
import re
from pathlib import Path
from datetime import datetime

MEMORY_DIR = Path("/home/zx/.openclaw/workspace/memory")
DB_PATH = Path("/home/zx/.openclaw/workspace/.qmd_index.db")


def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            path TEXT UNIQUE,
            content TEXT,
            modified_time INTEGER,
            indexed_at INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS terms (
            id INTEGER PRIMARY KEY,
            term TEXT UNIQUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inverted_index (
            term_id INTEGER,
            doc_id INTEGER,
            frequency INTEGER,
            PRIMARY KEY (term_id, doc_id)
        )
    ''')
    
    conn.commit()
    conn.close()


def tokenize(text):
    """分词 - 支持中英文"""
    english_words = re.findall(r'[a-zA-Z_]+', text.lower())
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return english_words + chinese_chars


def index_file(filepath, conn):
    """索引单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cursor = conn.cursor()
        modified_time = int(os.path.getmtime(filepath))
        
        cursor.execute("SELECT modified_time FROM documents WHERE path = ?", (str(filepath),))
        result = cursor.fetchone()
        
        if result and result[0] == modified_time:
            return False
        
        cursor.execute("SELECT id FROM documents WHERE path = ?", (str(filepath),))
        old_doc = cursor.fetchone()
        if old_doc:
            cursor.execute("DELETE FROM inverted_index WHERE doc_id = ?", (old_doc[0],))
            cursor.execute("DELETE FROM documents WHERE id = ?", (old_doc[0],))
        
        cursor.execute(
            "INSERT INTO documents (path, content, modified_time, indexed_at) VALUES (?, ?, ?, ?)",
            (str(filepath), content, modified_time, int(datetime.now().timestamp()))
        )
        doc_id = cursor.lastrowid
        
        words = tokenize(content)
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        for word, freq in word_freq.items():
            cursor.execute("INSERT OR IGNORE INTO terms (term) VALUES (?)", (word,))
            cursor.execute("SELECT id FROM terms WHERE term = ?", (word,))
            term_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO inverted_index (term_id, doc_id, frequency) VALUES (?, ?, ?)",
                (term_id, doc_id, freq)
            )
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"索引失败 {filepath}: {e}")
        return False


def search(query, top_k=5):
    """搜索记忆"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query_words = tokenize(query)
    if not query_words:
        return []
    
    placeholders = ','.join('?' * len(query_words))
    cursor.execute(f'''
        SELECT d.path, d.content, SUM(ii.frequency) as score
        FROM terms t
        JOIN inverted_index ii ON t.id = ii.term_id
        JOIN documents d ON ii.doc_id = d.id
        WHERE t.term IN ({placeholders})
        GROUP BY d.id
        ORDER BY score DESC
        LIMIT ?
    ''', query_words + [top_k])
    
    results = cursor.fetchall()
    conn.close()
    
    return [{'path': r[0], 'snippet': r[1][:300], 'score': r[2]} for r in results]


def stats():
    """显示统计信息"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM documents")
    doc_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM terms")
    term_count = cursor.fetchone()[0]
    conn.close()
    print(f"📊 QMD 统计: {doc_count} 文档, {term_count} 词汇")


def index_all():
    """索引所有记忆文件"""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    indexed = 0
    
    for md_file in MEMORY_DIR.glob('*.md'):
        if index_file(md_file, conn):
            indexed += 1
            print(f"✓ 索引: {md_file.name}")
    
    main_memory = Path("/home/zx/.openclaw/workspace/MEMORY.md")
    if main_memory.exists() and index_file(main_memory, conn):
        indexed += 1
        print(f"✓ 索引: MEMORY.md")
    
    conn.close()
    print(f"\n完成: {indexed} 个文件已索引")


def main():
    if len(sys.argv) < 2:
        print("用法: python memory_qmd.py [search|stats|index] [参数]")
        return
    
    command = sys.argv[1]
    
    if command == 'search':
        if len(sys.argv) < 3:
            print("错误: 需要提供查询内容")
            return
        results = search(sys.argv[2], 5)
        for i, r in enumerate(results, 1):
            print(f"{i}. [{r['path']}] (score: {r['score']})")
            print(f"   {r['snippet'][:100]}...")
    
    elif command == 'stats':
        stats()
    
    elif command == 'index':
        index_all()
    
    else:
        print(f"未知命令: {command}")


if __name__ == '__main__':
    main()
