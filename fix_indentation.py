#!/usr/bin/env python3
"""
Script to fix indentation issues in Python files.
Converts all tabs to 4 spaces and fixes mixed indentation.
"""

def fix_indentation(filename, output_filename=None):
    """Fix indentation issues in a Python file."""
    if output_filename is None:
        output_filename = filename.replace('.py', '_fixed.py')
    
    try:
        # Read the file
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into lines
        lines = content.splitlines()
        fixed_lines = []
        
        for line_num, line in enumerate(lines, 1):
            # Convert tabs to 4 spaces
            fixed_line = line.expandtabs(4)
            fixed_lines.append(fixed_line)
            
            print(f"Line {line_num}: {repr(line[:50])} -> {repr(fixed_line[:50])}")
        
        # Write the fixed content
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(fixed_lines))
        
        print(f"\n✅ Fixed file saved as: {output_filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing file: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    # You can specify your filename here
    filename = "Moviessbot.py"  # Change this to your actual filename
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    print(f"🔧 Fixing indentation in: {filename}")
    success = fix_indentation(filename)
    
    if success:
        print("\n🎉 Indentation fixed! Use the '_fixed.py' file.")
    else:
        print("\n💡 Make sure the file exists and try again.")