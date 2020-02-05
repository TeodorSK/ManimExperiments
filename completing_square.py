from manimlib.imports import *
import os
import pyclbr

#TODO: maybe replace these with u/v, flash a/b to avoid confusion with std form
class ExpandingPSTrinomial(Scene):
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

class ExpandingPSTrinomialExample(Scene):
    def construct(self):
        LS = TexMobject("2","(","x","+","1",")","^2","-","3")
        eq = TexMobject("=")
        RS_init = LS.copy()
        eq_group = VGroup(LS, eq, RS_init)
        eq_group.scale(1.5)
        eq_group.arrange_submobjects(RIGHT)

        RS_exp1=TexMobject("2","(","x","^2","+","2","x","+","1",")","-","3").move_to(RS_init).match_dim_size(RS_init,0)
        RS_exp2=TexMobject("2","x","^2","+","4","x","+","2","-","3").move_to(RS_init).match_dim_size(RS_init,0)
        RS_final = TexMobject("2","x","^2","+","4","x","-","1").move_to(RS_init).match_dim_size(RS_init,0)




        self.play(Write(LS))
        self.play(Write(eq))

        self.play(ReplacementTransform(LS.copy(),RS_init))
        self.play(ReplacementTransform(RS_init, RS_exp1))
        self.play(ReplacementTransform(RS_exp1, RS_exp2))
        self.play(ReplacementTransform(RS_exp2, RS_final))

        self.play()

class Comparing(GraphScene):
    CONFIG = {
        "plane_kwargs" : {
        "x_line_frequency" : 2,
        "y_line_frequency" :2
        },
        "functions" : [
            lambda x: 2*(x+1)**2-3],
        "color_main" : YELLOW,
        "center_point" : 0,
        "x_min" : -6,
        "x_max" : 4,
        "y_min" : -4,
        "y_max" : 5,
        "graph_origin" : DOWN,
        "y_axis_height": 4,
        "x_axis_width": 4,
        # "x_labeled_nums" : range(-2, 4, 2),
        "area_opacity": 0.2,
    }
    def construct(self):

        my_plane=NumberPlane(**self.plane_kwargs)
        my_plane.add(my_plane.get_axis_labels())
        # self.add(my_plane)
        # Show/hide grid for debugging
        self.setup_axes(animate=True)


        std_form_text = TextMobject("Standard form").set_color(GREEN)
        std_form_eq = TexMobject("2","x","^2","+","4","x","-","1")
        std_form = VGroup(std_form_text, std_form_eq)
        std_form.arrange_submobjects(DOWN).shift(2*UP+4*LEFT)
        vert_form_text = TextMobject("Vertex form").shift(2*UP+4*RIGHT).set_color(BLUE)
        vert_form_eq = TexMobject("2","(","x","+","1",")","^2","-","3")

        vert_form = VGroup(vert_form_text, vert_form_eq)
        vert_form.arrange_submobjects(DOWN).shift(2*UP+4*RIGHT)

        graph1 = self.get_graph(self.functions[0],TEAL)

        self.play(
            Write(std_form_text),
            Write(std_form_eq),
            Write(vert_form_text),
            Write(vert_form_eq),
            ShowCreation(graph1),
        )
        self.wait()

        self.play(
            FadeOut(self.axes),
            FadeOut(graph1),
            ApplyMethod(vert_form.shift, DOWN+LEFT),
            ApplyMethod(std_form.shift, DOWN+RIGHT),
        )
        self.play(
            ApplyMethod(vert_form.scale, 1.5),
            ApplyMethod(std_form.scale, 1.5),
        )

        self.play(
            FadeOut(std_form_eq),
            FadeOut(vert_form_eq),
        )


        vert_form_blank = TexMobject("a","(","x","-","h",")","^2","+","k").next_to(vert_form_text,DOWN)
        vert_form_uv = TexMobject("(","u","+","v",")","^2").next_to(vert_form_blank, DOWN)
        std_form_blank = TexMobject("a","x","^2","+","b","x","+","c").next_to(std_form_text,DOWN)
        std_form_uv = TexMobject("u","^2","+","2","u","v","+","v","^2").next_to(std_form_blank, DOWN)
        self.play(Write(vert_form_blank),Write(std_form_blank))
        self.play(Write(vert_form_uv),Write(std_form_uv))

        #pointers
        pointer_vert_std = CurvedArrow(3*LEFT+0.5*DOWN,3*RIGHT+0.5*DOWN,color=YELLOW).flip()
        expand_text = TextMobject("Expanding").next_to(pointer_vert_std, DOWN)
        pointer_std_vert = CurvedArrow(3*LEFT+0.5*DOWN,3*RIGHT+0.5*DOWN,color=YELLOW)
        compl_sqr_text = TextMobject("\"Completing the square\"").next_to(pointer_std_vert,DOWN)
        self.play(Write(pointer_vert_std),Write(expand_text))
        self.play(FadeOut(pointer_vert_std),FadeOut(expand_text))
        self.play(Write(pointer_std_vert),Write(compl_sqr_text))
        self.play(FadeOut(pointer_std_vert),FadeOut(compl_sqr_text))

        #highlighting
        self.play(
            ApplyMethod(std_form_uv[0:2].set_color, RED),
            ApplyMethod(std_form_blank[1:3].set_color, RED),
        )
        self.play(
            ApplyMethod(std_form_uv[4].set_color, RED),
            ApplyMethod(std_form_blank[5].set_color, RED),
        )
        self.play(
            ApplyMethod(vert_form_uv[1].set_color, RED),
            ApplyMethod(vert_form_blank[2].set_color, RED),
        )
        self.play(
            ApplyMethod(vert_form_uv[0].set_color, RED),
            ApplyMethod(vert_form_blank[1].set_color, RED),
            ApplyMethod(vert_form_uv[4:6].set_color, RED),
            ApplyMethod(vert_form_blank[5:7].set_color, RED),
        )


class Completing1(Scene):
    CONFIG = {

    }
    def construct(self):
        std_pattern = TexMobject("u","^2","+","2","u","v","+","v","^2").shift(UP)
        std_simple = TexMobject("(","u","+","v",")","^2").shift(UP)
        middle_term_uv = TexMobject("2","u","v").next_to(std_pattern[4],3*UP).scale(1.5)
        middle_term_uv_vsq = TexMobject("v^2").move_to(middle_term_uv[2]).scale(1.5)
        vert_pattern = TexMobject("(","u","+","v",")","^2")
        eq = TexMobject("x","^2","+","6","x","+","5").next_to(std_pattern,DOWN, buff=LARGE_BUFF)
        eq_21 = TexMobject("x","^2","+","6","x","+","3^2", "+","5").move_to(eq).align_to(eq,LEFT)
        eq_22 = TexMobject("x","^2","+","6","x","+","3^2", "-","3^2","+","5").move_to(eq).align_to(eq,LEFT)
        eq_2s = TexMobject("x","^2","+","6","x","+","9", "-","4").move_to(eq).align_to(eq,LEFT)
        eq_fin = TexMobject("(","x","+","3",")","^2","-","4").move_to(eq).align_to(eq,LEFT)
        middle_term_eq = TexMobject("6","x").next_to(eq[4],3*DOWN+0.5*LEFT).scale(1.5)
        middle_term_eq2 = TexMobject("2","\cdot","3","\cdot","x").move_to(middle_term_eq).scale(1.5)
        middle_term_3sq = TexMobject("3^2").move_to(middle_term_eq2[2]).scale(1.5)
        question = TextMobject("???").next_to(std_pattern[7],DOWN*1.6)
        yay = TextMobject("Yay!").next_to(eq,2*DOWN).scale(1.5).set_color(GREEN)

        self.play(Write(eq))
        self.play(Write(std_pattern))

        #flash 1st term
        self.play(
            ApplyMethod(eq[0:2].set_color,RED),
            ApplyMethod(std_pattern[0:2].set_color,RED),
        )
        self.play(
            ApplyMethod(eq[0:2].set_color,WHITE),
            ApplyMethod(std_pattern[0:2].set_color,WHITE),
        )

        #flash 2nd term
        self.play(
            ApplyMethod(eq[3:5].set_color,RED),
            ApplyMethod(std_pattern[3:6].set_color,RED),
        )
        self.play(
            ApplyMethod(eq[3:5].set_color,WHITE),
            ApplyMethod(std_pattern[3:6].set_color,WHITE),
        )

        #grey 3rd term
        self.play(Write(question))
        self.play(FadeOut(question))
        self.play(
            ApplyMethod(eq[6].set_color,DARK_GREY),
            ApplyMethod(std_pattern[7:9].set_color,DARK_GREY),
        )

        #isolate b
        self.play(ReplacementTransform(std_pattern[3:6].copy(), middle_term_uv),)
        self.play(ReplacementTransform(eq[3:5].copy(), middle_term_eq),)
        self.play(ReplacementTransform(middle_term_eq, middle_term_eq2))

        self.play(FadeOut(middle_term_eq2[0:2]),FadeOut(middle_term_uv[0:1]))
        self.play(FadeOut(middle_term_eq2[3:5]),FadeOut(middle_term_uv[1:2]))
        self.play(ReplacementTransform(middle_term_uv[2],middle_term_uv_vsq))
        self.play(ReplacementTransform(middle_term_eq2[2],middle_term_3sq))

        #match v^2 pattern
        self.play(ApplyMethod(middle_term_uv_vsq.replace,std_pattern[7:9]),path_arc=-1*np.pi)

        #add-sub 3^2
        self.play(
            ApplyMethod(eq[6].set_color,WHITE),
            ApplyMethod(std_pattern[:7].set_color,DARK_GREY),
            FadeOut(middle_term_uv_vsq))
        # self.remove(middle_term_uv_vsq)
        self.play(
            ReplacementTransform(middle_term_3sq.copy(),eq_21[6],path_arc=np.pi),
            ReplacementTransform(eq[6],eq_21[8]))
        self.play(
            ReplacementTransform(eq_21[8],eq_22[10]),
            ReplacementTransform(middle_term_3sq.copy(),eq_22[8],path_arc=np.pi),
            ReplacementTransform(eq_21[7],eq_22[7]),
            FadeIn(eq_22[9]))

        #simplify
        self.remove(eq_21[6])
        self.play(
            ReplacementTransform(eq_22[6],eq_2s[6]),
            ReplacementTransform(eq_22[7:11],eq_2s[7:9]),
            FadeOut(middle_term_3sq))

        #highlight trinomial
        self.play(ApplyMethod(std_pattern.set_color,WHITE))
        self.play(
            ApplyMethod(std_pattern.set_color,RED),
            ApplyMethod(eq_2s[0:7].set_color,RED),
        )

        self.play(ReplacementTransform(std_pattern,std_simple))
        self.remove(*eq_21)
        self.remove(*eq_22)
        self.remove(*eq)
        self.play(
            ReplacementTransform(eq_2s[0:7],eq_fin[0:6]),
            ReplacementTransform(eq_2s[7:9],eq_fin[6:8])
        )
        self.play(ApplyMethod(eq_fin.set_color,GREEN))
        self.play(Write(yay),FadeOut(std_simple))



if __name__ == "__main__":
    ###Using Python class browser to determine which classes are defined in this file
    module_name = 'completing_square'   #Name of current file
    module_info = pyclbr.readmodule(module_name)

    for item in module_info.values():
        if item.module==module_name:
            print(item.name)
            os.system("python -m manim completing_square.py %s -l" % item.name)  #Does not play files
