# System automation module for physical operations
class SystemAutomation:
    def create_text_file(self, filename: str, content: str) -> str:
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            return f"File '{filename}' created successfully."
        except Exception as e:
            return f"Failed to create file: {str(e)}"