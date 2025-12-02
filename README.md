Per tutti i file .ply e per le cartelle icp_results e icp_noFilter_results ho usato Git LFS.
Ho utilizzato due tipi di ICP, il primo (main_ICP.py) ho usato un filtro molto più restrittivo, nel secondo (main_ICP_noFilter.py) meno rigido. 
Ho usato questi filtri perchè si formava una piccola nuvola di punti molto lontana rispetto al corpo principale della mappa.
Ho usato solo ICP perchè solo utilizzando questo tipo di algoritmo la sua compilazione è stata notevolmente lunga (5984.58 secondi e 6464.98 secondi), quindi con RANSAC+FPFH i tempi sarebbero stati infinitamente più lunghi
