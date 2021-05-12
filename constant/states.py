idle=[0x10F,0xC47]
normal_fish=[0x112,0xc49]
small_big=[0x113,0xc4a]
bite=[0x124,0x125,0x126]

states = {
    0: "idle",
    1: "normal_fish",
    2: "small_big",
    3: "light_bite",
    4: "medium_bite",
    5: "heavy_bite",
    6: "other",
    7: "unknown"
}
opcode_list= {
    '0x10f': 0,
    '0xc47': 0,
    '0x112': 1,
    '0xc49': 1,
    '0x113': 2,
    '0xc4a': 2,
    '0x124': 3,
    '0x125': 4,
    '0x126': 5,
    '0x1234':6,
    '0x1233':6,
    '0x0':6,
    '0x11b':6
}
def get_states(op_code):
    #print(int(op_code))
    op_type=opcode_list.get(op_code,7)
    op_states=states[op_type]
    print(op_states)
    return op_type
