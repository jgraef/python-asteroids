
def singleton(cls):
    instance_container = []
    def __getinstance__(*args, **kargs):
        if len(instance_container)==0:
            instance_container.append(cls(*args, **kargs))
        return instance_container[0]
    return __getinstance__
