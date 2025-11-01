#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script test lay schema cua bang Spend.GIAODICH_FINAL
"""

import sys
import os

# Them duong dan src vao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import database_connector as db_conn

print("=" * 60)
print("TEST LAY SCHEMA BANG: Spend.GIAODICH_FINAL")
print("=" * 60)

# Test 1: Lay danh sach database
print("\n1. Lay danh sach database...")
databases = db_conn.lay_danh_sach_database()
print(f"   Tim thay {len(databases)} database:")
for db in databases:
    print(f"   - {db}")

# Test 2: Lay danh sach bang tu database 'Spend' (neu co)
if 'Spend' in databases:
    print("\n2. Lay danh sach bang trong database 'Spend'...")
    tables = db_conn.lay_danh_sach_bang('Spend')
    print(f"   Tim thay {len(tables)} bang:")
    for table in tables[:10]:  # Chi hien thi 10 bang dau
        print(f"   - {table}")
    if len(tables) > 10:
        print(f"   ... va {len(tables) - 10} bang khac")
else:
    print("\n2. Khong tim thay database 'Spend'")

# Test 3: Lay schema cua bang 'Spend.GIAODICH_FINAL'
print("\n3. Lay schema cua bang 'Spend.GIAODICH_FINAL'...")
try:
    schema = db_conn.lay_schema_bang('Spend.GIAODICH_FINAL', 'Spend')
    print(f"   Tim thay {len(schema)} cot:")
    for col in schema[:5]:  # Chi hien thi 5 cot dau
        print(f"   - {col['column_name']:30} {col['sql_type']:15} -> Tableau: {col['tableau_type']}")
    if len(schema) > 5:
        print(f"   ... va {len(schema) - 5} cot khac")
    
    if len(schema) == 0:
        print("\n   ❌ LOI: Schema RONG - khong co cot nao!")
    else:
        print(f"\n   ✅ SUCCESS: Schema co {len(schema)} cot")
        
except Exception as e:
    print(f"   ❌ LOI: {e}")

print("\n" + "=" * 60)
print("KET THUC TEST")
print("=" * 60)
