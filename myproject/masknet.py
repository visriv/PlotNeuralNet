
import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

arch = [ 
    to_head('.'), 
    to_cor(),
    to_begin(),
    
    #input
    to_input( 'ct_scan.png', to = '(-3, 0,0)', name = 'img1'),
    to_input( 'pet_scan.png', to = '(-2,0,0)', name = 'img2'),

    #block-001
    to_Conv( name='conv1', s_filer=48, n_filer=1, offset="(0,0,0)", to="(0,0,0)", width=2, height=32, depth=32, opacity=1, colorfill = "\PurpleColor"),
    to_BN(name="bn1", offset="(0,0,0)", to="(conv1-east)", width=1, height=32, depth=32, opacity=1),
    
    *block_ConvBN( name='b2', botton='bn1', top='pool_b2', s_filer=48, n_filer=48, offset="(4,0,0)", size=(32,32,1), opacity=1.0 ),
    *block_ConvBN( name='b3', botton='pool_b2', top='pool_b3', s_filer=48, n_filer=96, offset="(4,0,0)", size=(32,32,2), opacity=1.0 ),
    *block_ConvBN( name='b4', botton='pool_b3', top='pool_b4', s_filer=48,  n_filer=144, offset="(5,0,0)", size=(32,32,4), opacity=1.0 ),

    to_Sum( 'sum2', offset="(2,7,0)", to="(pool_b3-east)", radius=2.5, opacity=0.6, fill = "\GreenColor"),
    to_Sum( 'sum3', offset="(2,7,0)", to="(pool_b4-east)", radius=2.5, opacity=0.6, fill = "\GreenColor"),
    to_connection( "sum2", "sum3"),

    to_skip( of='pool_b4', to='sum3', pos=1.25),    


    #Bottleneck
    #block-005
    to_ConvConvRelu( name='ccr_b5', s_filer=32, n_filer=(1024,1024), offset="(2,0,0)", to="(pool_b4-east)", width=(8,8), height=8, depth=8, caption="Bottleneck"  ),
    to_connection( "pool_b4", "ccr_b5"),

    #Decoder
    *block_Unconv( name="b6", botton="ccr_b5", top='end_b6', s_filer=64,  n_filer=512, offset="(2.1,0,0)", size=(16,16,5.0), opacity=0.5 ),
    #to_skip( of='ccr_b4', to='ccr_res_b6', pos=1.25),
    *block_Unconv( name="b7", botton="end_b6", top='end_b7', s_filer=128, n_filer=256, offset="(2.1,0,0)", size=(25,25,4.5), opacity=0.5 ),
    #to_skip( of='ccr_b3', to='ccr_res_b7', pos=1.25),    
    *block_Unconv( name="b8", botton="end_b7", top='end_b8', s_filer=256, n_filer=128, offset="(2.1,0,0)", size=(32,32,3.5), opacity=0.5 ),
    #to_skip( of='ccr_b2', to='ccr_res_b8', pos=1.25),    
    
    *block_Unconv( name="b9", botton="end_b8", top='end_b9', s_filer=512, n_filer=64,  offset="(2.1,0,0)", size=(40,40,2.5), opacity=0.5 ),
    #to_skip( of='ccr_b1', to='ccr_res_b9', pos=1.25),
    
    to_ConvSoftMax( name="soft1", s_filer=512, offset="(0.75,0,0)", to="(end_b9-east)", width=1, height=40, depth=40, caption="SOFT" ),
    to_connection( "end_b9", "soft1"),
     
    to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.txt' )

if __name__ == '__main__':
    main()
    
