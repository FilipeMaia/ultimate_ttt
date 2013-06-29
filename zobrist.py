def init_zobrist():
    table = {}
    for i in range(1,3):
        table[i] = np.zeros((9,9),dtype=np.uint64)
        table[i] += np.random.random_integers(np.iinfo(np.uint32).min,high=np.iinfo(np.uint32).max,size=[9,9])
        table[i] <<= 32
        table[i] += np.random.random_integers(np.iinfo(np.uint32).min,high=np.iinfo(np.uint32).max,size=[9,9])
    return table

state['zobrist'] = init_zobrist()
state['ttable_size'] = 1e6
state['ttable_key'] = np.zeros(state['ttable_size'],dtype=np.uint64)
state['ttable_value'] = np.zeros(state['ttable_size'])

def ttable_get(key,state):
    print key
    print "key type = %s" % (type(key))
    entry = key%state['ttable_size']
    print entry
    print "entry type = %s" % (type(entry))
    
    if(state['ttable_key'][entry] == key):
        return state['ttable_value'][entry]
    return None

def ttable_insert(val,key,state):
    entry = np.mod(key,state['ttable_size'])
    state['ttable_value'][entry] = val
    state['ttable_key'][entry] = key

def ttable_key(state):
    x = np.zeros(1,dtype=np.uint64)
    o = np.zeros(1,dtype=np.uint64)
    a = state['zobrist'][1][np.where(state['board'] == 1)]
    if(len(a)):
        x = np.bitwise_xor.reduce(a)
    a = state['zobrist'][2][np.where(state['board'] == 2)]
    print type(a)
    print a.dtype
    if(len(a)):
        o = np.bitwise_xor.reduce(a)
    key = np.bitwise_xor(x,o)[0]
    return key



    # Don't use tranposition table
    # Too complicated for too little gain
#    key = ttable_key(state)
#    ttable_value = ttable_get(key,state)
#    if(ttable_value is not None):
#        print "TT hit!"
#        return ttable_value,[]


#        ttable_insert(val,key,state)



