#!/usr/bin/env python3
"""
Model Context Protocol (MCP) Demo Examples
==========================================

This file contains practical examples of MCP servers for demonstration purposes.
Each example shows a different aspect of MCP and can be run independently.

Requirements:
- mcp package (pip install mcp)
- aiohttp (for API examples)
- pathlib (built-in)
"""

import asyncio
import json
import aiohttp
import sqlite3
from pathlib import Path
from typing import Dict, List, Any
import os
from datetime import datetime

# =============================================================================
# Example 1: Basic File System MCP Server
# =============================================================================

class FileSystemMCPServer:
    """
    A simple MCP server that provides file system access.
    Demonstrates: Resources, Tools, and basic MCP structure.
    """
    
    def __init__(self, root_directory: str = "."):
        self.root = Path(root_directory).resolve()
        self.name = "FileSystem MCP Server"
        self.version = "1.0.0"
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """List all files as resources"""
        resources = []
        try:
            for file_path in self.root.rglob("*"):
                if file_path.is_file():
                    relative_path = file_path.relative_to(self.root)
                    resources.append({
                        "uri": f"file://{relative_path}",
                        "name": file_path.name,
                        "description": f"File: {relative_path}",
                        "mimeType": self._get_mime_type(file_path)
                    })
        except Exception as e:
            print(f"Error listing resources: {e}")
        return resources
    
    async def read_resource(self, uri: str) -> str:
        """Read a file resource"""
        try:
            # Extract path from URI
            path = uri.replace("file://", "")
            file_path = self.root / path
            
            if not file_path.exists():
                return f"Error: File not found: {path}"
            
            if not file_path.is_file():
                return f"Error: Not a file: {path}"
            
            # Security check: ensure path is within root
            if not str(file_path.resolve()).startswith(str(self.root)):
                return "Error: Access denied - path outside root directory"
            
            return file_path.read_text(encoding='utf-8', errors='ignore')
        
        except Exception as e:
            return f"Error reading file: {e}"
    
    async def list_files_tool(self, directory: str = ".") -> Dict[str, Any]:
        """Tool: List files in a directory"""
        try:
            dir_path = self.root / directory
            
            if not dir_path.exists():
                return {"error": f"Directory not found: {directory}"}
            
            if not dir_path.is_dir():
                return {"error": f"Not a directory: {directory}"}
            
            files = []
            for item in dir_path.iterdir():
                files.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None,
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                })
            
            return {"files": files, "directory": str(directory)}
        
        except Exception as e:
            return {"error": f"Error listing files: {e}"}
    
    async def create_file_tool(self, path: str, content: str) -> Dict[str, Any]:
        """Tool: Create a new file with content"""
        try:
            file_path = self.root / path
            
            # Security check
            if not str(file_path.resolve().parent).startswith(str(self.root)):
                return {"error": "Access denied - path outside root directory"}
            
            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            file_path.write_text(content, encoding='utf-8')
            
            return {
                "success": True,
                "message": f"File created: {path}",
                "size": len(content)
            }
        
        except Exception as e:
            return {"error": f"Error creating file: {e}"}
    
    async def search_files_tool(self, pattern: str, directory: str = ".") -> Dict[str, Any]:
        """Tool: Search for files matching a pattern"""
        try:
            dir_path = self.root / directory
            matches = []
            
            for file_path in dir_path.rglob(pattern):
                if file_path.is_file():
                    relative_path = file_path.relative_to(self.root)
                    matches.append({
                        "path": str(relative_path),
                        "name": file_path.name,
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
            
            return {
                "pattern": pattern,
                "directory": directory,
                "matches": matches,
                "count": len(matches)
            }
        
        except Exception as e:
            return {"error": f"Error searching files: {e}"}
    
    def _get_mime_type(self, file_path: Path) -> str:
        """Get MIME type based on file extension"""
        extension = file_path.suffix.lower()
        mime_types = {
            '.txt': 'text/plain',
            '.md': 'text/markdown',
            '.py': 'text/x-python',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.html': 'text/html',
            '.css': 'text/css',
            '.xml': 'application/xml',
            '.yaml': 'application/x-yaml',
            '.yml': 'application/x-yaml',
        }
        return mime_types.get(extension, 'application/octet-stream')


# =============================================================================
# Example 2: API Integration MCP Server
# =============================================================================

class WeatherMCPServer:
    """
    MCP server that integrates with weather APIs.
    Demonstrates: External API integration, error handling, and data processing.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.name = "Weather MCP Server"
        self.version = "1.0.0"
    
    async def get_current_weather_tool(self, city: str, units: str = "metric") -> Dict[str, Any]:
        """Tool: Get current weather for a city"""
        if not self.api_key:
            return {"error": "API key not configured"}
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "city": data["name"],
                            "country": data["sys"]["country"],
                            "temperature": data["main"]["temp"],
                            "feels_like": data["main"]["feels_like"],
                            "humidity": data["main"]["humidity"],
                            "pressure": data["main"]["pressure"],
                            "description": data["weather"][0]["description"],
                            "wind_speed": data.get("wind", {}).get("speed", 0),
                            "visibility": data.get("visibility", 0) / 1000,  # Convert to km
                            "timestamp": datetime.now().isoformat(),
                            "units": units
                        }
                    elif response.status == 404:
                        return {"error": f"City not found: {city}"}
                    else:
                        return {"error": f"API request failed: {response.status}"}
        
        except Exception as e:
            return {"error": f"Error fetching weather: {e}"}
    
    async def get_weather_forecast_tool(self, city: str, days: int = 5) -> Dict[str, Any]:
        """Tool: Get weather forecast for a city"""
        if not self.api_key:
            return {"error": "API key not configured"}
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "cnt": days * 8  # 8 forecasts per day (every 3 hours)
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        forecast = []
                        
                        for item in data["list"]:
                            forecast.append({
                                "datetime": item["dt_txt"],
                                "temperature": item["main"]["temp"],
                                "description": item["weather"][0]["description"],
                                "humidity": item["main"]["humidity"],
                                "wind_speed": item.get("wind", {}).get("speed", 0)
                            })
                        
                        return {
                            "city": data["city"]["name"],
                            "country": data["city"]["country"],
                            "forecast": forecast,
                            "total_forecasts": len(forecast)
                        }
                    else:
                        return {"error": f"API request failed: {response.status}"}
        
        except Exception as e:
            return {"error": f"Error fetching forecast: {e}"}
    
    async def weather_alert_prompt(self, city: str, threshold_temp: float) -> str:
        """Prompt: Generate weather alert template"""
        return f"""
        Create a weather alert for {city} with the following criteria:
        
        Temperature Threshold: {threshold_temp}°C
        
        Please use the get_current_weather_tool to check the current weather
        and generate an alert if:
        1. Temperature exceeds the threshold
        2. There are severe weather conditions (storms, heavy rain, etc.)
        3. Visibility is poor (< 1km)
        4. Wind speed is high (> 20 km/h)
        
        Format the alert as:
        - Alert level (LOW/MEDIUM/HIGH)
        - Conditions causing the alert
        - Recommendations for safety
        - When to check again
        """


# =============================================================================
# Example 3: Database MCP Server
# =============================================================================

class DatabaseMCPServer:
    """
    MCP server for database operations.
    Demonstrates: Database integration, structured data, and complex tools.
    """
    
    def __init__(self, db_path: str = "demo.db"):
        self.db_path = db_path
        self.name = "Database MCP Server"
        self.version = "1.0.0"
        self._init_database()
    
    def _init_database(self):
        """Initialize demo database with sample data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price DECIMAL(10,2),
                category TEXT,
                stock INTEGER DEFAULT 0
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)
        
        # Insert sample data if tables are empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            sample_users = [
                ("Alice Johnson", "alice@example.com"),
                ("Bob Smith", "bob@example.com"),
                ("Carol Davis", "carol@example.com")
            ]
            cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", sample_users)
            
            sample_products = [
                ("Laptop", 999.99, "Electronics", 10),
                ("Mouse", 29.99, "Electronics", 50),
                ("Desk Chair", 149.99, "Furniture", 5),
                ("Notebook", 4.99, "Office", 100)
            ]
            cursor.executemany("INSERT INTO products (name, price, category, stock) VALUES (?, ?, ?, ?)", sample_products)
        
        conn.commit()
        conn.close()
    
    async def execute_query_tool(self, query: str, params: List[Any] = None) -> Dict[str, Any]:
        """Tool: Execute a SQL query"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                rows = cursor.fetchall()
                result = [dict(row) for row in rows]
                return {
                    "success": True,
                    "data": result,
                    "row_count": len(result),
                    "query": query
                }
            else:
                conn.commit()
                return {
                    "success": True,
                    "rows_affected": cursor.rowcount,
                    "query": query
                }
        
        except Exception as e:
            return {"error": f"Database error: {e}"}
        finally:
            conn.close()
    
    async def get_table_schema_tool(self, table_name: str) -> Dict[str, Any]:
        """Tool: Get schema information for a table"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            if not columns:
                return {"error": f"Table '{table_name}' not found"}
            
            schema = []
            for col in columns:
                schema.append({
                    "name": col[1],
                    "type": col[2],
                    "not_null": bool(col[3]),
                    "default_value": col[4],
                    "primary_key": bool(col[5])
                })
            
            return {
                "table": table_name,
                "columns": schema,
                "column_count": len(schema)
            }
        
        except Exception as e:
            return {"error": f"Error getting schema: {e}"}
        finally:
            conn.close()
    
    async def list_tables_tool(self) -> Dict[str, Any]:
        """Tool: List all tables in the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            return {
                "tables": tables,
                "count": len(tables)
            }
        
        except Exception as e:
            return {"error": f"Error listing tables: {e}"}
        finally:
            conn.close()
    
    async def create_order_tool(self, user_id: int, product_id: int, quantity: int) -> Dict[str, Any]:
        """Tool: Create a new order"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            if not cursor.fetchone():
                return {"error": f"User with id {user_id} not found"}
            
            # Check if product exists and has enough stock
            cursor.execute("SELECT stock FROM products WHERE id = ?", (product_id,))
            result = cursor.fetchone()
            if not result:
                return {"error": f"Product with id {product_id} not found"}
            
            stock = result[0]
            if stock < quantity:
                return {"error": f"Insufficient stock. Available: {stock}, Requested: {quantity}"}
            
            # Create order
            cursor.execute("""
                INSERT INTO orders (user_id, product_id, quantity)
                VALUES (?, ?, ?)
            """, (user_id, product_id, quantity))
            
            order_id = cursor.lastrowid
            
            # Update stock
            cursor.execute("""
                UPDATE products SET stock = stock - ?
                WHERE id = ?
            """, (quantity, product_id))
            
            conn.commit()
            
            return {
                "success": True,
                "order_id": order_id,
                "user_id": user_id,
                "product_id": product_id,
                "quantity": quantity,
                "message": f"Order {order_id} created successfully"
            }
        
        except Exception as e:
            return {"error": f"Error creating order: {e}"}
        finally:
            conn.close()


# =============================================================================
# Example 4: System Information MCP Server
# =============================================================================

class SystemInfoMCPServer:
    """
    MCP server for system information and monitoring.
    Demonstrates: System integration, real-time data, and monitoring tools.
    """
    
    def __init__(self):
        self.name = "System Information MCP Server"
        self.version = "1.0.0"
    
    async def get_system_info_tool(self) -> Dict[str, Any]:
        """Tool: Get basic system information"""
        try:
            import platform
            import psutil
            
            return {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "architecture": platform.architecture()[0],
                "processor": platform.processor(),
                "hostname": platform.node(),
                "python_version": platform.python_version(),
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total,
                "memory_available": psutil.virtual_memory().available,
                "disk_usage": {
                    "total": psutil.disk_usage('/').total,
                    "used": psutil.disk_usage('/').used,
                    "free": psutil.disk_usage('/').free
                },
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {"error": f"Error getting system info: {e}"}
    
    async def get_process_list_tool(self, limit: int = 10) -> Dict[str, Any]:
        """Tool: Get list of running processes"""
        try:
            import psutil
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage and limit results
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            processes = processes[:limit]
            
            return {
                "processes": processes,
                "total_shown": len(processes),
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {"error": f"Error getting process list: {e}"}
    
    async def run_command_tool(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Tool: Run a system command (with safety restrictions)"""
        import subprocess
        
        # Safety: only allow safe commands
        safe_commands = [
            'ls', 'dir', 'pwd', 'date', 'whoami', 'uname',
            'ps', 'df', 'free', 'uptime', 'which', 'echo'
        ]
        
        command_parts = command.split()
        if not command_parts or command_parts[0] not in safe_commands:
            return {"error": f"Command not allowed: {command_parts[0] if command_parts else 'empty'}"} 
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "command": command,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
        
        except subprocess.TimeoutExpired:
            return {"error": f"Command timed out after {timeout} seconds"}
        except Exception as e:
            return {"error": f"Error running command: {e}"}


# =============================================================================
# Demo Runner and Test Functions
# =============================================================================

async def demo_filesystem_server():
    """Demonstrate the FileSystem MCP Server"""
    print("🗂️  FileSystem MCP Server Demo")
    print("=" * 50)
    
    server = FileSystemMCPServer(".")
    
    # List resources
    print("\n📋 Available Resources:")
    resources = await server.list_resources()
    for resource in resources[:5]:  # Show first 5
        print(f"  - {resource['name']} ({resource['uri']})")
    
    # List files tool
    print(f"\n📁 Files in current directory:")
    files_result = await server.list_files_tool(".")
    if "files" in files_result:
        for file_info in files_result["files"][:5]:
            print(f"  - {file_info['name']} ({file_info['type']}) - {file_info.get('size', 0)} bytes")
    
    # Search files
    print(f"\n🔍 Searching for Python files:")
    search_result = await server.search_files_tool("*.py")
    if "matches" in search_result:
        print(f"  Found {search_result['count']} Python files")
        for match in search_result["matches"][:3]:
            print(f"  - {match['name']} ({match['size']} bytes)")
    
    # Create a demo file
    print(f"\n📝 Creating demo file:")
    create_result = await server.create_file_tool("demo_output.txt", "Hello from MCP Demo!")
    print(f"  Result: {create_result}")


async def demo_weather_server():
    """Demonstrate the Weather MCP Server"""
    print("\n🌤️  Weather MCP Server Demo")
    print("=" * 50)
    
    # Note: This demo will show structure without actual API calls
    server = WeatherMCPServer()  # Will work if API key is set
    
    print("\n🌍 Getting weather for London:")
    weather_result = await server.get_current_weather_tool("London")
    print(f"  Result: {weather_result}")
    
    print("\n📅 Weather forecast template:")
    prompt = await server.weather_alert_prompt("New York", 30.0)
    print(f"  Prompt: {prompt[:200]}...")


async def demo_database_server():
    """Demonstrate the Database MCP Server"""
    print("\n🗄️  Database MCP Server Demo")
    print("=" * 50)
    
    server = DatabaseMCPServer()
    
    # List tables
    print("\n📊 Available tables:")
    tables_result = await server.list_tables_tool()
    print(f"  Tables: {tables_result}")
    
    # Get schema
    print("\n🏗️  Users table schema:")
    schema_result = await server.get_table_schema_tool("users")
    if "columns" in schema_result:
        for col in schema_result["columns"]:
            print(f"  - {col['name']} ({col['type']}) {'NOT NULL' if col['not_null'] else ''}")
    
    # Query data
    print("\n👥 All users:")
    users_result = await server.execute_query_tool("SELECT * FROM users")
    if "data" in users_result:
        for user in users_result["data"]:
            print(f"  - {user['name']} ({user['email']})")
    
    # Create an order
    print("\n🛒 Creating a sample order:")
    order_result = await server.create_order_tool(1, 1, 2)
    print(f"  Result: {order_result}")


async def demo_system_server():
    """Demonstrate the System Information MCP Server"""
    print("\n💻 System Information MCP Server Demo")
    print("=" * 50)
    
    server = SystemInfoMCPServer()
    
    # Get system info
    print("\n🖥️  System information:")
    sys_info = await server.get_system_info_tool()
    if "platform" in sys_info:
        print(f"  Platform: {sys_info['platform']} {sys_info.get('platform_version', '')}")
        print(f"  Architecture: {sys_info.get('architecture', 'Unknown')}")
        print(f"  CPU Count: {sys_info.get('cpu_count', 'Unknown')}")
        print(f"  Memory: {sys_info.get('memory_available', 0) / (1024**3):.1f}GB available")
    else:
        print(f"  Error: {sys_info}")
    
    # Get process list
    print("\n🔄 Top processes:")
    processes = await server.get_process_list_tool(5)
    if "processes" in processes:
        for proc in processes["processes"]:
            print(f"  - {proc['name']} (PID: {proc['pid']}) - CPU: {proc.get('cpu_percent', 0):.1f}%")
    
    # Run safe command
    print("\n🏃 Running 'echo' command:")
    cmd_result = await server.run_command_tool("echo 'Hello from MCP!'")
    print(f"  Output: {cmd_result.get('stdout', '').strip()}")


async def run_all_demos():
    """Run all MCP server demonstrations"""
    print("🚀 Model Context Protocol (MCP) Demo")
    print("=" * 60)
    print("This demo shows practical examples of MCP servers in action.")
    print("Each server demonstrates different aspects of the MCP protocol.")
    
    try:
        await demo_filesystem_server()
        await demo_weather_server()
        await demo_database_server()
        await demo_system_server()
        
        print("\n✅ All demos completed successfully!")
        print("\n🎯 Key Takeaways:")
        print("  - MCP standardizes AI access to external systems")
        print("  - Three primitives: Resources, Tools, and Prompts")
        print("  - Easy to build with Python/TypeScript SDKs")
        print("  - Secure by design with built-in controls")
        print("  - Composable and extensible architecture")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")


if __name__ == "__main__":
    # Install requirements message
    print("📦 Required packages:")
    print("  pip install mcp aiohttp psutil")
    print("\n🔑 Optional: Set OPENWEATHER_API_KEY environment variable for weather demo")
    print("\n" + "="*60)
    
    # Run the demos
    asyncio.run(run_all_demos())