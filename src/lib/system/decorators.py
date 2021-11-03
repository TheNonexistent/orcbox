import functools

def singleton(cls):
    @functools.wraps(cls)
    def singleton_wrapper(*args, **kwargs):
        if not singleton_wrapper.instance:
            singleton_wrapper.instance = cls(*args, **kwargs)
        
        return singleton_wrapper.instance
        
        singleton_wrapper.instance = None
        return singleton_wrapper
