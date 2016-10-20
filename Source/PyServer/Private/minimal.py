# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
def main_loop(gworld):
    while 1:
        print('in main loop')
        yield

def kill():
    print('done!')
