# -*- coding: utf-8 -*-
"""
Test ket noi SQL Server
Ho tro ca Windows va Linux
"""

import pyodbc
import json
import os
import sys

def tim_file_config():
    """Tim file config tu nhieu vi tri"""
    # Thu cac duong dan co the
    possible_paths = [
        "config/database_config.json",
        "../config/database_config.json",
        "../../config/database_config.json",
    ]
    
    # Thu tu vi tri script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    config_path_1 = os.path.join(project_dir, "config", "database_config.json")
    config_path_2 = os.path.join(script_dir, "..", "config", "database_config.json")
    
    possible_paths.insert(0, config_path_1)
    possible_paths.insert(1, config_path_2)
    
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            return abs_path
    
    return None

def test_connection():
    """Test ket noi"""
    print("=" * 60)
    print("TEST KET NOI SQL SERVER")
    print("=" * 60)
    print()
    
    # Tim file config
    config_file = tim_file_config()
    
    if not config_file:
        print("ERROR: Cannot find database_config.json")
        print()
        print("Please make sure config/database_config.json exists")
        return False
    
    print(f"Config file: {config_file}")
    print()
    
    # Doc config
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"ERROR reading config: {e}")
        return False
    
    # Lay thong tin
    server = config.get('server', '127.0.0.1')
    port = config.get('port', 1433)
    database = config.get('database', 'master')
    windows_auth = config.get('windows_auth', False)
    user = config.get('user', '')
    password = config.get('password', '')
    
    print(f"Server: {server}")
    print(f"Port: {port}")
    print(f"Database: {database}")
    print(f"Windows Auth: {windows_auth}")
    print()
    
    # Tao connection string
    if windows_auth:
        conn_str = f"DRIVER={{SQL Server}};SERVER={server},{port};DATABASE={database};Trusted_Connection=yes"
        print("Using Windows Authentication...")
    else:
        conn_str = f"DRIVER={{SQL Server}};SERVER={server},{port};DATABASE={database};UID={user};PWD={password}"
        print("Using SQL Server Authentication...")
    
    print()
    
    # Ket noi
    try:
        print("Connecting...")
        conn = pyodbc.connect(conn_str, timeout=10)
        cursor = conn.cursor()
        
        print()
        print("SUCCESS! Connected to SQL Server")
        print()
        
        # Test query
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print("SQL Server Version:")
        print(version[:80] + "...")
        print()
        
        # Check protocol
        cursor.execute("""
        SELECT net_transport, local_tcp_port
        FROM sys.dm_exec_connections 
        WHERE session_id = @@SPID
        """)
        
        row = cursor.fetchone()
        print(f"Protocol: {row[0]}")
        print(f"Port: {row[1]}")
        print()
        
        if row[0] == 'TCP' and row[1] == 1433:
            print("PERFECT! Using TCP/IP on port 1433")
        else:
            print("WARNING: Not using TCP/IP or wrong port")
        
        print()
        
        # List databases
        cursor.execute("""
        SELECT name FROM sys.databases 
        WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')
        ORDER BY name
        """)
        
        dbs = cursor.fetchall()
        print(f"Found {len(dbs)} databases")
        
        conn.close()
        
        print()
        print("=" * 60)
        print("TEST PASSED!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print()
        print("ERROR: Connection failed")
        print()
        print(str(e))
        print()
        
        if "Login failed" in str(e):
            print("Check username/password")
        elif "timeout" in str(e).lower():
            print("Check if SQL Server is running")
            print("Check if TCP/IP is enabled")
            print("Check firewall settings")
        
        return False

if __name__ == "__main__":
    success = test_connection()
    
    print()
    if sys.platform == 'win32':
        input("Press Enter to close...")
    
    sys.exit(0 if success else 1)
