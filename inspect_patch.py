# inspect_patch.py
import inspect
import functools

# Add getargspec back for compatibility
if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec
    
    # Monkey patch the import system
    _original_import = __import__
    
    @functools.wraps(_original_import)
    def _patched_import(name, globals=None, locals=None, fromlist=(), level=0):
        module = _original_import(name, globals, locals, fromlist, level)
        if name == 'inspect' or (fromlist and 'getargspec' in fromlist):
            if not hasattr(module, 'getargspec'):
                module.getargspec = inspect.getfullargspec
        return module
    
    __builtins__['__import__'] = _patched_import