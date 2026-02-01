"""
Utility functions for the application
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import json


class DateTimeUtils:
    """Utility functions for datetime operations"""
    
    @staticmethod
    def now() -> datetime:
        """Get current UTC datetime"""
        return datetime.utcnow()
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Format datetime object to string"""
        if dt is None:
            return None
        return dt.strftime(format_str)
    
    @staticmethod
    def iso_format(dt: datetime) -> str:
        """Get ISO format of datetime"""
        if dt is None:
            return None
        return dt.isoformat()
    
    @staticmethod
    def time_ago(dt: datetime) -> str:
        """Get human-readable time difference"""
        if dt is None:
            return "Unknown"
        
        now = datetime.utcnow()
        diff = now - dt
        
        if diff.days > 365:
            return f"{diff.days // 365} year(s) ago"
        elif diff.days > 30:
            return f"{diff.days // 30} month(s) ago"
        elif diff.days > 0:
            return f"{diff.days} day(s) ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} hour(s) ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} minute(s) ago"
        else:
            return "Just now"


class StringUtils:
    """Utility functions for string operations"""
    
    @staticmethod
    def truncate(text: str, max_length: int = 50, suffix: str = "...") -> str:
        """Truncate string to max length"""
        if not text or len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def normalize(text: str) -> str:
        """Normalize string (lowercase, strip whitespace)"""
        if not text:
            return text
        return text.strip().lower()
    
    @staticmethod
    def slugify(text: str) -> str:
        """Convert text to URL-friendly slug"""
        if not text:
            return ""
        
        import re
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')
    
    @staticmethod
    def highlight_search(text: str, search_term: str) -> str:
        """Highlight search term in text"""
        if not text or not search_term:
            return text
        
        import re
        pattern = re.compile(re.escape(search_term), re.IGNORECASE)
        return pattern.sub(f"**{search_term}**", text)


class ListUtils:
    """Utility functions for list/collection operations"""
    
    @staticmethod
    def chunk(items: List[Any], chunk_size: int) -> List[List[Any]]:
        """Split list into chunks"""
        return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
    
    @staticmethod
    def unique(items: List[Any]) -> List[Any]:
        """Get unique items preserving order"""
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    @staticmethod
    def flatten(nested_list: List[List[Any]]) -> List[Any]:
        """Flatten nested list"""
        result = []
        for item in nested_list:
            if isinstance(item, list):
                result.extend(ListUtils.flatten(item))
            else:
                result.append(item)
        return result


class DictUtils:
    """Utility functions for dictionary operations"""
    
    @staticmethod
    def get_nested(data: Dict, key_path: str, default: Any = None) -> Any:
        """Get nested dictionary value using dot notation"""
        keys = key_path.split('.')
        value = data
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
        
        return value if value is not None else default
    
    @staticmethod
    def filter_keys(data: Dict, keys: List[str]) -> Dict:
        """Filter dictionary to only include specified keys"""
        return {k: v for k, v in data.items() if k in keys}
    
    @staticmethod
    def exclude_keys(data: Dict, keys: List[str]) -> Dict:
        """Filter dictionary to exclude specified keys"""
        return {k: v for k, v in data.items() if k not in keys}
    
    @staticmethod
    def merge(*dicts: Dict) -> Dict:
        """Merge multiple dictionaries"""
        result = {}
        for d in dicts:
            result.update(d)
        return result


class ValidationUtils:
    """Utility functions for validation"""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email address"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate URL"""
        import re
        pattern = r'^https?:\/\/.+'
        return re.match(pattern, url) is not None
    
    @staticmethod
    def is_valid_uuid(value: str) -> bool:
        """Validate UUID"""
        import re
        pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return re.match(pattern, value, re.I) is not None


class PaginationUtils:
    """Utility functions for pagination"""
    
    @staticmethod
    def calculate_offset(page: int, page_size: int) -> int:
        """Calculate offset from page number"""
        if page < 1:
            page = 1
        return (page - 1) * page_size
    
    @staticmethod
    def calculate_pages(total: int, page_size: int) -> int:
        """Calculate total number of pages"""
        if page_size <= 0:
            return 0
        return (total + page_size - 1) // page_size
    
    @staticmethod
    def get_pagination_info(
        total: int,
        page: int = 1,
        page_size: int = 10
    ) -> Dict[str, int]:
        """Get complete pagination information"""
        pages = PaginationUtils.calculate_pages(total, page_size)
        offset = PaginationUtils.calculate_offset(page, page_size)
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
            "offset": offset,
            "has_next": page < pages,
            "has_prev": page > 1
        }


# Export all utilities
__all__ = [
    'DateTimeUtils',
    'StringUtils',
    'ListUtils',
    'DictUtils',
    'ValidationUtils',
    'PaginationUtils',
]
