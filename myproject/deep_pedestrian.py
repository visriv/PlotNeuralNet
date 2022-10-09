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
    to_input( 'pet_scan.png', to = '(-2,0,0)', name = 'img2'),

    #block-01x
    *block_4Conv( name='conv1', to='(0,0,0)', s_filer=256, n_filer=(2,48,48,48), offset="(0,0,0)", height=24, depth=24, widths=(1,3.5,3.5,3.5), opacity=0.5 ),
    *block_4Conv( name='conv2', to='(cccc_conv1-east)', s_filer=256, n_filer=(48,48,48,48), offset="(1,0,0)", height=24, depth=24, widths=(3.5,3.5,3.5,3.5), opacity=0.5 ),
     to_connection( "cccc_conv1", "cccc_conv2"),

     to_Fusion("add1", 256, 1, offset="(1,0,0)", to="(cccc_conv2-east)", height=24, depth=24, width=1, caption='add'),

     # to_Sum( 'sum1', offset="(1,0,0)", to="(cccc_conv2-east)", radius=1, opacity=0.6),

     to_skip( "cccc_conv1", "add1"),
     to_connection( "cccc_conv2", "add1"),

     #block-02x
    *block_4Conv( name='conv3', to='(add1-east)', s_filer=256, n_filer=(48,48,48,48), offset="(1,0,0)", height=24, depth=24, widths=(1,3.5,3.5,3.5), opacity=0.5 ),
     to_connection( "add1", "cccc_conv3"),
    *block_4Conv( name='conv4', to='(cccc_conv3-east)', s_filer=256, n_filer=(48,48,48,48), offset="(1,0,0)", height=24, depth=24, widths=(3.5,3.5,3.5,3.5), opacity=0.5 ),
     to_connection( "cccc_conv3", "cccc_conv4"),

     to_Fusion("add2", 256, 1, offset="(1,0,0)", to="(cccc_conv4-east)", height=24, depth=24, width=1, caption='add'),

     # to_Sum( 'sum1', offset="(1,0,0)", to="(cccc_conv2-east)", radius=1, opacity=0.6),

     to_skip( "cccc_conv3", "add2"),
     to_connection( "cccc_conv4", "add2"),

     to_SoftMax("conv5", 256, offset="(1,0,0)", to="(add2-east)", height=24, depth=24, width=1 ),
     to_connection( "add2", "conv5"),







    to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.txt' )

if __name__ == '__main__':
    main()