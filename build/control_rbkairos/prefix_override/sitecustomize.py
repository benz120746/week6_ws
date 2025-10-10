import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/khotkangplue_p/week6_ws/install/control_rbkairos'
