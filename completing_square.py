from manimlib.imports import *
import os
import pyclbr

class CompletingSquare(Scene):
    CONFIG = {

    }

    def construct(self):
        LS = TexMobject("(","a","+","b",")","^2")
        eq = TexMobject("=")
        RS = TexMobject("a","^2","+","a","b","+","a","b","+","b","^2")
        eq_group = VGroup(LS, eq, RS)
        eq_group.scale(1.5)
        eq_group.arrange_submobjects(RIGHT)
        RS_simple = TexMobject("a","^2","+","2","ab","+","b","^2").move_to(RS).match_dim_size(RS,1)

        self.play(Write(LS))
        self.play(Write(eq))

        self.play( #tween a^2
            ReplacementTransform(LS[1].copy(), RS[0],path_arc=np.pi),
            ReplacementTransform(LS[1].copy(), RS[0],path_arc=-1*np.pi),
            FadeIn(RS[1])
        )
        self.play( #tween ab
            FadeIn(RS[2]),
            ReplacementTransform(LS[1].copy(), RS[3],path_arc=np.pi),
            ReplacementTransform(LS[3].copy(), RS[4],path_arc=-1*np.pi),
        )
        self.play( #tween ab
            FadeIn(RS[5]),
            ReplacementTransform(LS[1].copy(), RS[6],path_arc=np.pi),
            ReplacementTransform(LS[3].copy(), RS[7],path_arc=-1*np.pi),
        )
        self.play( #tween a^2
            FadeIn(RS[8]),
            ReplacementTransform(LS[3].copy(), RS[9],path_arc=np.pi),
            ReplacementTransform(LS[3].copy(), RS[9],path_arc=-1*np.pi),
            FadeIn(RS[10]),
        )
        self.play( #tween simplify
            ReplacementTransform(RS[0:3],RS_simple[0:3]),
            ReplacementTransform(RS[3:8],RS_simple[3:5]),
            ReplacementTransform(RS[8:11],RS_simple[5:8]),
            #Note: ranges need to be end-inclusive
        )
        RS_simple.bg = SurroundingRectangle(RS_simple,color=BLUE,)
        self.play(
            # ApplyMethod(RS_simple.surround,)
            Write(RS_simple.bg)
        )

        self.wait()

if __name__ == "__main__":
    ###Using Python class browser to determine which classes are defined in this file
    module_name = 'completing_square'   #Name of current file
    module_info = pyclbr.readmodule(module_name)

    for item in module_info.values():
        if item.module==module_name:
            print(item.name)
            os.system("python -m manim completing_square.py %s -l" % item.name)  #Does not play files
