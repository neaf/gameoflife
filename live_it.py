from gameoflife import evolve

def draw(cells):                                                            
    rows = [] 
    for x in range(-60, 60): 
        row = [] 
        for y in range(-60, 60): 
            if (y, x) in cells: 
                row.append('##') 
            else:                                                           
                row.append('  ')                                            
        rows.append(''.join(row))                                           
    print '\n'.join(rows) 
 
if __name__ == "__main__": 
    from time import sleep 
 
    cells = [(1,1), (1,2), (3,2), (2,4), (1,5), (1,6), (1,7)] 
 
    while True: 
        draw(cells) 
        cells = evolve(cells) 
        sleep(0.03) 
