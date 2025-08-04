#!/usr/bin/env python3
"""
Simplified Model Context Protocol (MCP) Demo
============================================

This demo shows MCP concepts without requiring external packages.
It demonstrates the three core primitives: Resources, Tools, and Prompts.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class SimpleMCPDemo:
    """
    A simplified demonstration of MCP concepts.
    This is NOT a full MCP implementation - just a conceptual demo.
    """
    
    def __init__(self):
        self.name = "Simple MCP Demo"
        self.version = "1.0.0"
        self.root = Path(".")
    
    # =============================================================================
    # RESOURCES: Static information that provides context
    # =============================================================================
    
    def list_resources(self) -> List[Dict[str, Any]]:
        """List available resources (files in current directory)"""
        resources = []
        
        for file_path in self.root.glob("*.py"):
            if file_path.is_file():
                resources.append({
                    "uri": f"file://{file_path.name}",
                    "name": file_path.name,
                    "description": f"Python file: {file_path.name}",
                    "mimeType": "text/x-python",
                    "size": file_path.stat().st_size
                })
        
        return resources[:5]  # Limit for demo
    
    def read_resource(self, uri: str) -> str:
        """Read a resource by URI"""
        try:
            # Extract filename from URI
            filename = uri.replace("file://", "")
            file_path = self.root / filename
            
            if not file_path.exists():
                return f"Error: File not found: {filename}"
            
            # Read and return content (first 500 chars for demo)
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            return content[:500] + "..." if len(content) > 500 else content
        
        except Exception as e:
            return f"Error reading file: {e}"
    
    # =============================================================================
    # TOOLS: Interactive functions the AI can call
    # =============================================================================
    
    def list_files_tool(self, pattern: str = "*") -> Dict[str, Any]:
        """Tool: List files matching a pattern"""
        try:
            files = []
            for file_path in self.root.glob(pattern):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    files.append({
                        "name": file_path.name,
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                        "type": "file"
                    })
                elif file_path.is_dir() and not file_path.name.startswith('.'):
                    files.append({
                        "name": file_path.name,
                        "type": "directory",
                        "items": len(list(file_path.iterdir()))
                    })
            
            return {
                "pattern": pattern,
                "files": files[:10],  # Limit for demo
                "count": len(files)
            }
        
        except Exception as e:
            return {"error": f"Error listing files: {e}"}
    
    def file_info_tool(self, filename: str) -> Dict[str, Any]:
        """Tool: Get detailed information about a file"""
        try:
            file_path = self.root / filename
            
            if not file_path.exists():
                return {"error": f"File not found: {filename}"}
            
            stat = file_path.stat()
            
            info = {
                "name": file_path.name,
                "path": str(file_path),
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "is_file": file_path.is_file(),
                "is_directory": file_path.is_dir()
            }
            
            if file_path.is_file():
                info["extension"] = file_path.suffix
                # Count lines if it's a text file
                try:
                    if file_path.suffix in ['.py', '.txt', '.md', '.json']:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            info["lines"] = sum(1 for _ in f)
                except:
                    pass
            
            return info
        
        except Exception as e:
            return {"error": f"Error getting file info: {e}"}
    
    def calculator_tool(self, expression: str) -> Dict[str, Any]:
        """Tool: Safe calculator (basic operations only)"""
        try:
            # Simple safety check - only allow basic math operations
            allowed_chars = set('0123456789+-*/(). ')
            if not all(c in allowed_chars for c in expression):
                return {"error": "Invalid characters in expression"}
            
            # Evaluate safely (eval is normally dangerous, but we've restricted input)
            result = eval(expression)
            
            return {
                "expression": expression,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {"error": f"Calculation error: {e}"}
    
    def create_demo_file_tool(self, content: str = None) -> Dict[str, Any]:
        """Tool: Create a demo file"""
        try:
            if content is None:
                content = f"""# MCP Demo File
# Created: {datetime.now().isoformat()}

def mcp_greeting():
    '''A function created by MCP demo'''
    return "Hello from Model Context Protocol!"

def fibonacci(n):
    '''Calculate fibonacci number'''
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

if __name__ == "__main__":
    print(mcp_greeting())
    print(f"Fibonacci(10) = {{fibonacci(10)}}")
"""
            
            filename = f"mcp_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
            file_path = self.root / filename
            
            file_path.write_text(content, encoding='utf-8')
            
            return {
                "success": True,
                "filename": filename,
                "size": len(content),
                "message": f"Demo file '{filename}' created successfully"
            }
        
        except Exception as e:
            return {"error": f"Error creating file: {e}"}
    
    # =============================================================================
    # PROMPTS: Templates for common interactions
    # =============================================================================
    
    def analyze_project_prompt(self) -> str:
        """Prompt: Template for project analysis"""
        return """
Please analyze the current project structure and provide insights:

**Instructions:**
1. Use list_files_tool("*") to see all files
2. Use file_info_tool(filename) for detailed info on key files
3. Use read_resource(uri) to examine important files

**Analysis Framework:**

📊 **Project Overview**
- What type of project is this?
- What programming languages are used?
- What's the main purpose?

📁 **Structure Assessment**
- How well organized are the files?
- Are there clear separation of concerns?
- Any missing important files (README, tests, docs)?

⚡ **Recommendations**
- Suggested improvements
- Best practices to implement
- Missing components to add

**Format your response with clear sections and actionable insights.**
"""
    
    def code_review_prompt(self, filename: str) -> str:
        """Prompt: Template for code review"""
        return f"""
Please perform a comprehensive code review of '{filename}':

**Instructions:**
1. First, use file_info_tool("{filename}") to get file details
2. Then use read_resource("file://{filename}") to read the code
3. If there are calculations, verify them with calculator_tool()

**Review Framework:**

🔍 **Code Quality**
- Readability and clarity
- Code organization
- Naming conventions
- Comments and documentation

🏗️ **Best Practices**
- Language-specific conventions
- Design patterns usage
- Error handling
- Performance considerations

🛡️ **Potential Issues**
- Bugs or logical errors
- Security concerns
- Edge cases not handled
- Code smells

💡 **Recommendations**
- Specific improvements
- Refactoring suggestions
- Testing recommendations

**Rate each category (1-5 stars) and provide specific examples.**
"""
    
    def explain_mcp_prompt(self) -> str:
        """Prompt: Template for explaining MCP"""
        return """
Explain the Model Context Protocol (MCP) in simple terms:

**Use this structure:**

🎯 **What is MCP?**
- Simple definition
- Main purpose
- Key benefits

🏗️ **How does it work?**
- Client-server architecture
- JSON-RPC communication
- The three primitives

📖 **Real-world examples**
- Common use cases
- Popular implementations
- Business benefits

🚀 **Getting started**
- First steps for developers
- Available tools and SDKs
- Community resources

**Make it accessible for both technical and non-technical audiences.**
"""


def run_demo():
    """Run the complete MCP demo"""
    print("🚀 Model Context Protocol (MCP) Demo")
    print("=" * 60)
    print("This demo illustrates MCP concepts with practical examples.")
    print("Each section shows one of the three MCP primitives in action.\n")
    
    # Create demo instance
    demo = SimpleMCPDemo()
    
    # =============================================================================
    # RESOURCES Demo
    # =============================================================================
    print("📁 RESOURCES: Static context information")
    print("-" * 50)
    
    resources = demo.list_resources()
    print(f"Found {len(resources)} Python file resources:")
    
    for i, resource in enumerate(resources, 1):
        print(f"  {i}. {resource['name']} ({resource['size']} bytes)")
    
    if resources:
        print(f"\n📖 Reading resource: {resources[0]['name']}")
        content = demo.read_resource(resources[0]['uri'])
        print(f"Content preview:\n{content[:200]}...\n")
    
    # =============================================================================
    # TOOLS Demo
    # =============================================================================
    print("🔧 TOOLS: Interactive functions")
    print("-" * 50)
    
    # Tool 1: List files
    print("🗂️ Tool 1: Listing all files")
    files_result = demo.list_files_tool("*")
    if "files" in files_result:
        print(f"Found {files_result['count']} items:")
        for file_info in files_result["files"][:5]:
            if file_info["type"] == "file":
                print(f"  📄 {file_info['name']} ({file_info['size']} bytes)")
            else:
                print(f"  📁 {file_info['name']} ({file_info.get('items', 0)} items)")
    
    # Tool 2: Calculator
    print(f"\n🧮 Tool 2: Calculator")
    calc_examples = ["2 + 3 * 4", "(10 + 5) / 3", "2 ** 8"]
    for expr in calc_examples:
        result = demo.calculator_tool(expr)
        if "result" in result:
            print(f"  {expr} = {result['result']}")
        else:
            print(f"  {expr} → Error: {result['error']}")
    
    # Tool 3: Create demo file
    print(f"\n📝 Tool 3: Creating demo file")
    create_result = demo.create_demo_file_tool()
    if create_result.get("success"):
        print(f"  ✅ {create_result['message']}")
        
        # Get info about the created file
        file_info = demo.file_info_tool(create_result["filename"])
        if "lines" in file_info:
            print(f"  📊 File has {file_info['lines']} lines")
    else:
        print(f"  ❌ Error: {create_result.get('error')}")
    
    # =============================================================================
    # PROMPTS Demo
    # =============================================================================
    print(f"\n💬 PROMPTS: Structured interaction templates")
    print("-" * 50)
    
    # Prompt 1: Project analysis
    print("🔍 Prompt 1: Project Analysis Template")
    project_prompt = demo.analyze_project_prompt()
    print(project_prompt[:300] + "...\n")
    
    # Prompt 2: Code review
    if create_result.get("success"):
        print(f"📝 Prompt 2: Code Review Template for '{create_result['filename']}'")
        review_prompt = demo.code_review_prompt(create_result["filename"])
        print(review_prompt[:300] + "...\n")
    
    # Prompt 3: MCP explanation
    print("🎓 Prompt 3: MCP Explanation Template")
    explain_prompt = demo.explain_mcp_prompt()
    print(explain_prompt[:300] + "...\n")
    
    # =============================================================================
    # Summary
    # =============================================================================
    print("✨ Demo Complete!")
    print("=" * 60)
    print("🎯 Key Takeaways:")
    print("  • RESOURCES provide static context (files, docs, schemas)")
    print("  • TOOLS enable dynamic interactions (APIs, operations)")
    print("  • PROMPTS offer structured templates (workflows, analysis)")
    print("  • All three work together for powerful AI integrations")
    print("\n🌟 MCP Benefits:")
    print("  • Standardized protocol for all AI integrations")
    print("  • Built-in security and permission controls")
    print("  • Easy composability and reusability")
    print("  • Growing ecosystem of tools and clients")
    print("\n📚 Learn More:")
    print("  • Official docs: https://modelcontextprotocol.io")
    print("  • GitHub: https://github.com/modelcontextprotocol")
    print("  • Examples: https://github.com/modelcontextprotocol/servers")


if __name__ == "__main__":
    run_demo()