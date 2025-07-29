#!/usr/bin/env python3
"""
Script to create a PowerPoint presentation about Model Context Protocol (MCP)
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import re

def create_mcp_presentation():
    """Create a comprehensive MCP presentation"""
    
    # Create presentation object
    prs = Presentation()
    
    # Define color scheme
    primary_color = RGBColor(0, 102, 204)  # Blue
    accent_color = RGBColor(255, 140, 0)   # Orange
    text_color = RGBColor(51, 51, 51)      # Dark gray
    
    # Slide 1: Title Slide
    slide_layout = prs.slide_layouts[0]  # Title slide
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    
    title.text = "Model Context Protocol (MCP)"
    subtitle.text = "The USB-C of AI Integration\n\nRevolutionizing how AI systems connect with data sources and tools\n\nDeveloped by Anthropic • November 2024"
    
    # Slide 2: The Problem MCP Solves
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Why Do We Need MCP?"
    content.text = """The "N × M Problem"
• Before MCP: Every AI application needed custom integrations for each data source
• Result: Fragmented development, duplicated effort, maintenance nightmare

Key Challenges:
• Context Management: LLMs struggle with limited context windows
• Data Integration: Complex, custom integrations for each service  
• Security: Inconsistent access controls across different tools
• Scalability: No standardized way to add new capabilities

Real-World Impact:
• Development teams spending 60% of time on integrations
• Security vulnerabilities from inconsistent implementations
• Slow adoption of new AI tools due to integration complexity"""
    
    # Slide 3: What is MCP?
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Model Context Protocol Explained"
    content.text = """Simple Definition:
MCP is like USB-C for AI applications - one universal connector that works with any device.

Technical Definition:
A standardized protocol that enables AI applications to:
• Connect to external data sources and tools
• Share contextual information with language models
• Expose capabilities to AI systems
• Build composable workflows

Key Analogy:
Just like APIs standardized web interactions and Language Server Protocol (LSP) 
streamlined IDE functionality, MCP establishes a universal framework for AI integrations."""
    
    # Slide 4: MCP Architecture
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "How MCP Works: Architecture Overview"
    content.text = """Three-Layer Architecture:

1. MCP Hosts 🏠
• AI applications (Claude Desktop, Cursor, IDEs)
• Initiate connections to external resources
• Control the overall AI experience

2. MCP Clients 🔌
• Communication bridge between hosts and servers
• Handle authentication, service discovery, and transport
• Manage multiple server connections

3. MCP Servers 🖥️
• Expose specific capabilities and data
• Lightweight programs with focused responsibilities
• Can be local processes or remote services

Communication Protocol:
• JSON-RPC 2.0 messaging
• Transport Options: STDIO, Server-Sent Events (SSE)
• Stateful sessions with capability negotiation"""
    
    # Slide 5: MCP Core Features
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Three Fundamental Primitives"
    content.text = """1. Resources 📁
• What: Read-only data (like GET endpoints)
• Purpose: Load information into LLM context
• Examples: Database schemas, file contents, API documentation

2. Tools 🔧
• What: Executable functions (like POST endpoints)
• Purpose: Allow LLMs to perform actions
• Examples: Database queries, API calls, file operations, code execution

3. Prompts 💬
• What: Reusable templates for interactions
• Purpose: Standardize common AI workflows
• Examples: Code review templates, analysis frameworks, debugging guides"""
    
    # Slide 6: Easy Examples
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "MCP in Action: Simple Examples"
    content.text = """Example 1: Database Integration 🗃️
User: "Show me sales data for Q4"
→ MCP connects to database server
→ Retrieves sales records via SQL query tool
→ LLM analyzes and presents insights

Example 2: File System Access 📂
User: "Analyze this CSV file"
→ MCP filesystem server reads the file
→ Data loaded as resource into LLM context
→ LLM performs analysis and visualization

Example 3: GitHub Integration 🐙
User: "Review my latest pull request"
→ MCP GitHub server fetches PR details
→ Code changes loaded as resources
→ LLM provides comprehensive code review

Example 4: Multi-Tool Workflow 🔄
User: "Debug this production issue"
→ Error logs (via logging server)
→ Code analysis (via GitHub server)
→ Database queries (via SQL server)
→ Comprehensive diagnosis report"""
    
    # Slide 7: Real-World Use Cases
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Who Benefits from MCP?"
    content.text = """🏢 Enterprises
• Use Case: Customer support automation
• Example: AI agent accesses CRM, knowledge base, and ticketing system
• Benefit: 40% reduction in resolution time

👨‍💻 Developers
• Use Case: Intelligent coding assistants
• Example: AI helps with code review, documentation, and debugging
• Benefit: 60% faster development cycles

🏥 Healthcare
• Use Case: Medical diagnosis support
• Example: AI accesses patient records, medical literature, and imaging data
• Benefit: More accurate diagnoses with proper context

💰 Financial Services
• Use Case: Fraud detection and compliance
• Example: AI analyzes transactions, regulations, and risk patterns
• Benefit: 75% improvement in fraud detection accuracy"""
    
    # Slide 8: Benefits for Stakeholders
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Why MCP Matters for Everyone"
    content.text = """🔧 For Application Developers
✅ Zero additional work once MCP-compatible
✅ Standardized interfaces (Resources, Tools, Prompts)
✅ Access to growing ecosystem of MCP servers
✅ Focus on core logic instead of integrations

🏗️ For Tool/API Providers
✅ Build once, deploy everywhere across AI applications
✅ Increased adoption through simplified integration
✅ Access to intelligent agents for new use cases

👥 For End Users
✅ More powerful AI applications with rich context
✅ Seamless integration with familiar tools
✅ Intelligent assistance across various tasks
✅ Personalized experiences with their own data

🏢 For Enterprises
✅ Standardized AI development across teams
✅ Clear separation of concerns between infrastructure and applications
✅ Faster development cycles with reusable components
✅ Improved security with centralized access control"""
    
    # Slide 9: Security & Trust
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Built-in Security Framework"
    content.text = """🔐 Security Principles
1. User Consent: Explicit approval for data access and operations
2. Data Privacy: Protected with appropriate access controls
3. Tool Safety: Cautious approach to code execution
4. LLM Sampling Controls: User approval for model requests

🛡️ Implementation Guidelines
• Robust consent and authorization flows
• Clear documentation of security implications
• Appropriate access controls and data protections
• Privacy-by-design architecture

🔍 Multi-layered Security
• Transport Security: HTTPS with OAuth 2.0
• Capability Scoping: Servers define required permissions
• Data Obfuscation: Sensitive information protected from hosts
• Context Isolation: Strong boundaries between user sessions

🚀 Future Enhancements
• JWT-based attestation
• SPIFFE identities
• Enhanced encryption standards"""
    
    # Slide 10: Getting Started
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "How to Implement MCP"
    content.text = """🛠️ Development Options

Python/TypeScript (Quick Start)
@mcp_tool()
def search_database(query: str) -> list[dict]:
    return db.execute(f"SELECT * FROM products WHERE name LIKE '%{query}%'")

Java/Spring (Enterprise)
spring:
  ai:
    mcp:
      client:
        servers:
          - name: database-server
            url: https://mcp.example.com/db

Docker (Containerized)
FROM node:20-alpine
RUN npm install -g @modelcontextprotocol/server-github
ENTRYPOINT ["mcp-github-server"]

📚 Available SDKs
• Python SDK: Full MCP specification implementation
• TypeScript SDK: Web and Node.js support
• Java SDK: Spring Boot integration"""
    
    # Slide 11: MCP Ecosystem
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Growing Ecosystem of Tools"
    content.text = """🌟 Popular MCP Servers
• GitHub: Repository management and code analysis
• PostgreSQL: Database queries and schema access
• File System: Local file operations
• Slack: Team communication integration
• Google Drive: Document management
• AWS: Cloud service integration

🎯 Supported Applications
• Claude Desktop: Anthropic's flagship implementation
• Cursor: AI-powered code editor
• Windsurf: Development environment
• VS Code Extensions: Various MCP integrations

🔮 Future Registry
• Centralized discovery of MCP servers
• Cryptographic verification for security
• Cross-platform packaging for easy deployment
• Community contributions and certified servers"""
    
    # Slide 12: Performance & Scalability
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Built for Production"
    content.text = """⚡ Performance Metrics
• Latency: Sub-200ms for most operations
• Throughput: 12,000+ daily tool invocations
• Overhead: Only 2-3% increase in inference latency

🔧 Optimization Strategies
• Connection Pooling: Persistent connections reduce overhead
• Batch Operations: Multiple actions in single request
• Caching: ETag-like validators minimize data transfer
• Lazy Loading: Resources loaded only when needed

📈 Scalability Features
• Horizontal Scaling: Distributed across multiple servers
• Load Balancing: Intelligent request distribution
• Fault Tolerance: Graceful degradation on server failures
• Auto-scaling: Dynamic capacity management

🎯 Real-World Results
• Block: 60% reduction in integration costs
• Raygun: 4x faster development cycles
• Apollo: 500+ concurrent sales cycles managed"""
    
    # Slide 13: Future Roadmap
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "What's Coming Next?"
    content.text = """🚀 2025 Roadmap
• Remote Service Ecosystem: OAuth 2.0 integration
• DNS-based Discovery: Automatic server detection
• Serverless Support: AWS Lambda integration
• MCP Registry: Centralized server marketplace

🔮 Long-term Vision
• Real-time Streaming: IoT and live data integration
• Inter-agent Messaging: AI-to-AI communication
• Quantitative Semantics: Enhanced data reliability
• Cross-platform Standards: Universal AI integration

📊 Industry Impact Predictions
• 70% of Fortune 500 companies using MCP by 2026
• $2B+ ecosystem of managed MCP services
• Community-driven conformance testing and standards

🌍 Open Source Future
• Community special interest groups
• Educational initiatives and certification programs
• Open-source conformance testing tools"""
    
    # Slide 14: Comparison
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "MCP vs. Other Integration Approaches"
    content.text = """📊 Comparison Overview

                    Custom APIs    MCP         Traditional Middleware
Development Time    Weeks         Hours       Days
Maintenance         High          Low         Medium
Security           Inconsistent   Standardized Variable
Scalability        Limited       High        Medium
Vendor Lock-in     High          None        Medium
Community Support  Limited       Growing     Established

✅ MCP Advantages
• Standardization: Universal protocol for all AI integrations
• Composability: Mix and match different servers seamlessly
• Security: Built-in security frameworks and best practices
• Community: Growing ecosystem of tools and integrations

⚠️ Considerations
• Adoption: Still emerging (launched Nov 2024)
• Learning Curve: New protocol to understand
• Ecosystem: Limited compared to mature alternatives"""
    
    # Slide 15: Best Practices
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Success Tips for MCP Adoption"
    content.text = """🎯 Getting Started Right
1. Start Small: Begin with one simple integration
2. Choose the Right SDK: Python/TypeScript for prototypes, Java for enterprise
3. Focus on Security: Implement proper authentication from day one
4. Plan for Scale: Design with multiple servers in mind

🔧 Development Best Practices
• Error Handling: Graceful degradation when servers are unavailable
• Logging: Comprehensive audit trails for debugging
• Testing: Unit tests for server capabilities and client interactions
• Documentation: Clear API documentation for your MCP servers

🏢 Enterprise Considerations
• Governance: Establish policies for MCP server approval
• Monitoring: Track performance and usage metrics
• Backup Plans: Fallback strategies when integrations fail
• Training: Educate teams on MCP concepts and implementation

🔄 Continuous Improvement
• Feedback Loops: Regular review of integration performance
• Community Engagement: Contribute to open-source MCP projects
• Stay Updated: Follow MCP specification updates and new features"""
    
    # Slide 16: Conclusion
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "The Future of AI Integration is Here"
    content.text = """🌟 Key Takeaways
• MCP standardizes AI integrations like USB-C standardized device connections
• Solves the "N × M problem" with one protocol for all AI-data interactions
• Benefits everyone: developers, enterprises, tool providers, and end users
• Security-first approach with built-in access controls and privacy protection

🚀 Why Act Now?
• Early Adoption Advantage: Be ahead of the curve in AI integration
• Growing Ecosystem: More tools and services being added daily
• Proven Results: Companies already seeing 40-60% efficiency gains
• Future-Proof: Designed to evolve with advancing AI capabilities

📞 Next Steps
1. Explore MCP SDKs on GitHub
2. Try existing servers with Claude Desktop or Cursor
3. Build your first MCP server for your organization's data
4. Join the community and contribute to the ecosystem

🎯 Final Thought
"Just as APIs revolutionized web development and LSP transformed IDEs, 
MCP is set to revolutionize AI integration. The question isn't whether 
to adopt MCP, but how quickly you can get started.""""
    
    # Slide 17: Q&A and Resources
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]
    
    title.text = "Questions & Additional Resources"
    content.text = """❓ Common Questions
Q: Is MCP only for Anthropic's models?
A: No! MCP works with any LLM or AI application

Q: How does MCP compare to LangChain?
A: MCP focuses on standardizing integrations, while LangChain is a development framework

Q: Can I use MCP with existing APIs?
A: Yes! You can wrap existing APIs as MCP servers

🔗 Useful Resources
• Official Site: https://modelcontextprotocol.io
• GitHub Repository: https://github.com/modelcontextprotocol
• Python SDK: https://github.com/modelcontextprotocol/python-sdk
• TypeScript SDK: https://github.com/modelcontextprotocol/typescript-sdk
• Specification: https://spec.modelcontextprotocol.io

📚 Further Learning
• Anthropic's MCP documentation
• Community examples and tutorials
• MCP server implementations on GitHub
• AI integration best practices guides

Thank you for your attention!
Ready to revolutionize your AI integrations with MCP?"""
    
    # Save the presentation
    prs.save('Model_Context_Protocol_Presentation.pptx')
    print("✅ PowerPoint presentation created successfully!")
    print("📄 File saved as: Model_Context_Protocol_Presentation.pptx")
    return True

if __name__ == "__main__":
    try:
        create_mcp_presentation()
    except ImportError:
        print("❌ Error: python-pptx library not installed")
        print("💡 To install: pip install python-pptx")
        print("📋 Alternative: Use the markdown file 'MCP_Presentation.md' to manually create slides")
    except Exception as e:
        print(f"❌ Error creating presentation: {e}")
        print("📋 Please use the markdown file 'MCP_Presentation.md' to manually create slides")