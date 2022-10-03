import sys
sys.path.append('../')

sys.path.append('./PlotNeuralNet')

from pycore.tikzeng import *
from pycore.blocks  import *

arch = [ 
    to_head('.'), 
    to_cor(),
    to_begin(),
    
    #input
    to_input( 'ct_scan.png', to = '(-3, 0,0)', name = 'img1'),
    to_input( 'pet_scan.png', to = '(-3,-16,0)', name = 'img2'),

    #block-01x
    to_Conv("conv11", 32, 16, offset="(0,0,0)", to="(0,0,0)", height=32, depth=32, width=16 ),
    to_Conv("conv12", 28, 32, offset="(1,0,0)", to="(conv11-east)", height=28, depth=28, width=32 ),
    to_connection( "conv11", "conv12"),

    #block-02x
    to_Conv("conv21", 32, 16, offset="(0,-16,0)", to="(0,0,0)", height=32, depth=32, width=16 ),
    to_Conv("conv22", 28, 32, offset="(1,0,0)", to="(conv21-east)", height=28, depth=28, width=32 ),
    to_connection( "conv21", "conv22"),

    #fusion
    to_Fusion("fusion", 28, 32, offset="(2,-8,0)", to="(conv12-east)", height=28, depth=28, width=32, caption = 'fusion'),
    to_connection( "conv12", "fusion"),
    to_connection( "conv22", "fusion"),

    #block-002
    to_Conv("conv3", 28, 32, offset="(3,0,0)", to="(fusion-east)", height=28, depth=28, width=32 ),
    to_connection( "fusion", "conv3"),

    to_Conv("conv4", 28, 16, offset="(4,0,0)", to="(conv3-east)", height=28, depth=28, width=16 ),
    to_connection( "conv3", "conv4"),

    to_SoftMax("tanh_final", 32, offset="(5,0,0)", to="(conv4-east)", height=32, depth=32, width=1, caption = 'tanh' ),
    to_connection( "conv4", "tanh_final"),





    to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.txt' )

if __name__ == '__main__':
    main()