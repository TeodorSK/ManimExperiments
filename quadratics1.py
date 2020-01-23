from manimlib.imports import *
import os
import pyclbr

class VertexFormRoots(GraphScene):
    CONFIG = {
        "plane_kwargs" : {
        "x_line_frequency" : 2,
        "y_line_frequency" :2
        },
        "functions" : [
            lambda x: x**2,
            lambda x: x**2 - 4,
            lambda x: 0,
            lambda x: 2*x**2,
            lambda x: 2*(x+1)**2,
            lambda x: 2*(x+1)**2-3],
        "color_main" : YELLOW,
        "center_point" : 0,
        "x_min" : -6,
        "x_max" : 4,
        "y_min" : -5,
        "y_max" : 5,
        "graph_origin" : 4*LEFT+1*UP,
        "y_axis_height": 4,
        "x_axis_width": 4,
        # "x_labeled_nums" : range(-2, 4, 2),
        "area_opacity": 0.2,
    }

    #do i rly have to implement this myself
    #TODO
    #maybe give it some safety if you're gonna use this often
    def change_text(self, init_text, new_string):
        return TexMobject(*new_string).move_to(init_text).match_color(init_text).match_dim_size(init_text,1)

    #doesn't write, just returns. write manually
    def write_abcs(self):
        avar_label = TexMobject("a")
        bvar_label = TexMobject("b")
        cvar_label = TexMobject("c")
        abc = VGroup(*avar_label, *bvar_label, *cvar_label)
        abc.move_to(self.eq)
        avar_label.align_to(self.eq[0],LEFT)
        bvar_label.align_to(self.eq[3],LEFT)
        cvar_label.align_to(self.eq[6],LEFT)
        abc.shift(0.5*DOWN)
        abc.set_color(YELLOW)

        #kinda like a return?
        self.abc=abc
        return abc

    #Writes standard form quadratic equation ax^2 + bx + c
    #doesn't write, just returns. write manually
    def write_eq(self,a,b,c):
        self.a = str(a)
        self.b = str(b)
        self.c = str(c)

        #Need to prep numbers for printing. maybe make that it's own method?
        a = str(a) if a>0 else "("+str(a)+")"
        b = str(b)if b>0 else "("+str(b)+")"
        c = str(c)if c>0 else "("+str(c)+")"

        eq = TexMobject(a, "x^2", "+", b,"x", "+", c)
        eq.move_to(3*UP+4*RIGHT)

        #does this need to be here since now we're returning eq now
        #Yes, if other methods want to reference to it
        self.eq = eq

        return eq

    def write_discriminant(self,a,b,c):
        eq = self.eq

        disc_value = int(b)**2 - 4*int(a)*int(c)

        #Need to prep numbers for printing. maybe make that it's own method?
        a = str(a) if int(a)>0 else "("+str(a)+")"
        b = str(b)if int(b)>0 else "("+str(b)+")"
        c = str(c)if int(c)>0 else "("+str(c)+")"

        discAvars = ["a","\cdot"+a]
        discBvars = ["b^2",b+"^2"]
        discCvars = ["c","\cdot"+c]
        discriminant = TexMobject(discBvars[0], " - 4", discAvars[0],discCvars[0])
        discriminant.set_color(RED)
        discriminant.scale(1.25)
        discriminant.next_to(eq, DOWN*4)

        self.play(Write(discriminant))
        disc_str = discriminant.tex_strings
        disc_str[0] = discBvars[1]
        disc_str[2] = discAvars[1]
        disc_str[3] = discCvars[1]

        # discriminant.target = TexMobject(*disc_str).move_to(discriminant).match_color(discriminant).match_dim_size(discriminant,1)
        discriminant.target = self.change_text(discriminant, disc_str)

        eq_copy = eq.copy()
        self.play(
            MoveToTarget(discriminant),
            Transform(eq_copy,discriminant.target),
            )

        self.remove(eq_copy)

        #Showing result
        disc_str_result = discriminant.tex_strings
        disc_str_result.extend(["=",str(disc_value)])
        print(disc_str_result)
        # discriminant.target = TexMobject(*disc_str_result).move_to(discriminant).match_color(discriminant).match_dim_size(discriminant,1).shift(LEFT)
        discriminant.target = self.change_text(discriminant, disc_str_result).shift(LEFT)

        self.play(MoveToTarget(discriminant))
        return discriminant

    ##EXAMPLE for transforming (doesnt work)
    def example(self):

            eqn1 = TextMobject("$f(x)=$", "$x^2$", "$+$", "$x$")


            self.add(eqn1)
            eqn1.move_to(2*DOWN)

            # eqn1_strings = eqn1[e.get_tex_string() for e in eqn1]
            # Next line works but implementation could change.
            self.wait(2)
            eqn1_strings = eqn1.tex_strings
            eqn1_strings[1] = "$3x^3$"
            eqn1.target = TextMobject(*eqn1_strings)

            eqn1.target.move_to(eqn1)
            # eqn1.target.move_to(3*UP)
            # Next line can shift into place but not rotate or scale.
            # eqn1.target = TexMobject(*eqn1_strings).shift(eqn1.get_center)

            self.play(MoveToTarget(eqn1))

    def division_tween(self):
        #DivisionTween
        test_eq1 = TexMobject("3","=","2","x")
        test_eq2 = TexMobject("{3", "\\over", "2}", "=", "x")
        self.play(Write(test_eq1))
        self.play(
            ReplacementTransform(test_eq1[0],test_eq2[0]),
            ReplacementTransform(test_eq1[1],test_eq2[3]),
            ReplacementTransform(test_eq1[2],test_eq2[2],path_arc=-1*np.pi),
            ReplacementTransform(test_eq1[3],test_eq2[4]),
            FadeIn(test_eq2[1]))

    def construct(self):

        my_plane = NumberPlane(**self.plane_kwargs)
        my_plane.add(my_plane.get_axis_labels())
        # self.add(my_plane)
        #Show/hide grid for debugging
        self.setup_axes(animate=False)

        #equations
        eq1 = TexMobject("y", "=", "x^2")
        eq2 = TexMobject("y", "=", "x^2", "-", "4")
        eq2_zero = TexMobject("0", "=", "x^2", "-", "4")
        eq3_pre = TexMobject("4", "=", "x^2")
        eq3 = TexMobject("\pm \sqrt{4}", "=", "x")
        eq4_pos = TexMobject("x = 2")
        eq4_neg = TexMobject("x = -2")
        #arrange equations into groups to apply scale/location
        eq_group1 = VGroup(eq1, eq2, eq2_zero, eq3_pre, eq3, eq4_pos, eq4_neg)
        eq_group1.scale(1.5)
        eq_group1.arrange_submobjects(DOWN, buff = MED_SMALL_BUFF)
        eq_group1.move_to(UP*0.5+3.5*RIGHT)

        eq1_copy = eq1.copy()
        eq5 = TexMobject("y=2x^2")
        eq5_2 = TexMobject("y=2(x+1)^2")
        eq5_3 = TexMobject("y=2(x+1)^2-3")
        eq5_zero = TexMobject("0","=2(x+1)^2","-","3")
        eq6 = TexMobject("3=2(x+1)^2")
        eq7 = TexMobject("\dfrac{3}{2}=(x+1)^2")
        eq8 = TexMobject("\pm\sqrt { \dfrac { 3 }{ 2 }  }  = x+1")
        eq9_1 = TexMobject("-1.225-1=x")
        eq9_2 = TexMobject("1.225-1=x")
        eq10_1 = TexMobject("-2.225=x")
        eq10_2 = TexMobject("0.225=x")
        eq_group2 = VGroup (eq5, eq5_2, eq5_3)
        eq_group2.scale(1.5)
        eq_group2.arrange_submobjects(DOWN, buff = MED_SMALL_BUFF)
        eq_group2.move_to(UP*0.5+3.5*RIGHT)
        eq5_3.shift(LEFT)
        eq_group3 = VGroup (eq5_zero, eq6, eq7, eq8, eq9_1, eq9_2, eq10_1, eq10_2)
        eq_group3.scale(1.5)
        eq_group3.arrange_submobjects(DOWN, buff = MED_SMALL_BUFF)

        eq_group4 = eq_group3[4:]



        #graphs
        graph1 = self.get_graph(self.functions[0],self.color_main)
        graph2 = self.get_graph(self.functions[1],YELLOW)
        x_axis = self.get_graph(self.functions[2],RED)
        root_highlight1 = Dot().move_to(self.input_to_graph_point(-2,graph2))
        root_highlight2 = Dot().move_to(self.input_to_graph_point(2,graph2))
        root1_label = TexMobject("-2, 0").set_color(RED).next_to(root_highlight1, UP)
        root2_label = TexMobject("2, 0").set_color(RED).next_to(root_highlight2, UP)

        graph3 = self.get_graph(self.functions[3],self.color_main)
        graph4 = self.get_graph(self.functions[4],self.color_main)
        graph5 = self.get_graph(self.functions[5],self.color_main)
        root_highlight3 = Dot().move_to(self.input_to_graph_point(-2.225,graph5))
        root_highlight4 = Dot().move_to(self.input_to_graph_point(0.225,graph5))
        root3_label = TexMobject("-2.255, 0").set_color(RED).next_to(root_highlight3, UP).shift(LEFT)
        root4_label = TexMobject("0.255, 0").set_color(RED).next_to(root_highlight4, UP).shift(RIGHT)


        #play
        self.play(Write(eq1), ShowCreation(graph1))
        self.play(ReplacementTransform(eq1,eq2),ReplacementTransform(graph1, graph2))
        self.play(ReplacementTransform(eq2.copy(), eq2_zero),FadeIn(root_highlight1), FadeIn(root_highlight2))
        self.play(ShowCreation(x_axis), ApplyMethod(eq2_zero[0].set_color, RED))
        self.play( #tween
            ReplacementTransform(
            eq2_zero[4], eq2_zero[0],
            path_arc = -1*np.pi,
            rate_func=smooth,
            run_time = 1.5
            ),
            FadeOut(eq2_zero[3]),
            FadeOut(eq2_zero[0]),
            FadeOut(x_axis)
        )
        eq3_pre.move_to(eq2_zero,LEFT)


        self.play(Transform(eq3_pre,eq3))

        eq4_pos.shift(LEFT)
        eq4_neg.next_to(eq4_pos, RIGHT)

        self.play(ReplacementTransform(eq3.copy(), eq4_pos))
        self.play(ReplacementTransform(eq3.copy(), eq4_neg))
        self.play(
            ApplyMethod(eq4_pos.set_color, RED),
            ApplyMethod(eq4_neg.set_color, RED))
        self.play(
            ApplyMethod(root_highlight1.set_color, RED),
            ApplyMethod(root_highlight2.set_color, RED),
            ReplacementTransform(eq4_neg.copy(),root_highlight1),
            ReplacementTransform(eq4_pos.copy(),root_highlight2),
            )

        self.play(Write(root1_label),Write(root2_label))

        #part 2 Play
        #TODO: fix: elements that are already faded out (red zero) flash before fading out again
        #Current fix: make a copy of the tweened equation, remove orginal, fadeout copy
        self.play(
            FadeOut(eq_group1),
            FadeOut(graph2),
            FadeOut(root_highlight1),
            FadeOut(root_highlight2),
            FadeOut(root1_label),
            FadeOut(root2_label),)

        #TODO: graph1, eq1 got replaced earlier. reset them
        graph1 = self.get_graph(self.functions[0],self.color_main)
        # eq1 = self.change_text(eq5.copy(), "x^2")

        self.play(ShowCreation(graph1), Write(eq1_copy))
        #TODO: graph3->4 weird path of transformation. make smooth right to left
        self.play(ReplacementTransform(graph1, graph3), ReplacementTransform(eq1_copy, eq5))
        self.play(ReplacementTransform(graph3, graph4), ReplacementTransform(eq5, eq5_2))
        self.play(ReplacementTransform(graph4, graph5), ReplacementTransform(eq5_2, eq5_3))
        self.play(ApplyMethod(eq5_3.shift, 3.5*UP))
        eq_group3.next_to(eq5_3,DOWN)
        self.play(
            ReplacementTransform(eq5_3.copy(), eq5_zero),
            FadeIn(root_highlight3),
            FadeIn(root_highlight4))
        self.play(ShowCreation(x_axis), ApplyMethod(eq5_zero[0].set_color, RED))
        # self.play(ReplacementTransform(eq5_zero, eq6)) #apply tween here?
        self.play( #tween
            ReplacementTransform(
            eq5_zero[3], eq5_zero[0],
            path_arc = -1*np.pi,
            rate_func=smooth,
            run_time = 1.5
            ),
            FadeOut(eq5_zero[2]),
            FadeOut(eq5_zero[0]),
            FadeOut(x_axis)
        )
        eq_group3[1:].shift(UP)
        eq6.move_to(eq5_zero, LEFT)
        self.play(ReplacementTransform(eq6, eq7))
        self.play(ReplacementTransform(eq7, eq8))
        eq_group4.shift(3*UP)
        self.remove(*eq5_zero)
        eq5_zero = self.change_text(eq5_zero, "3=2(x+1)^2").shift(LEFT*0.4)

        self.play(ApplyMethod(eq8.shift, 4*UP),FadeOut(eq5_3), FadeOut(eq5_zero))
        eq9_1.shift(LEFT*3)
        eq9_2.next_to(eq9_1, RIGHT)
        self.play(ReplacementTransform(eq8.copy(), eq9_1))
        eq10_1.move_to(eq9_1)
        self.play(ReplacementTransform(eq9_1, eq10_1))
        self.play(ReplacementTransform(eq8.copy(), eq9_2))
        eq10_2.move_to(eq9_2)
        self.play(ReplacementTransform(eq9_2, eq10_2))

        self.play(
            ApplyMethod(eq10_1.set_color, RED),
            ApplyMethod(eq10_2.set_color, RED))
        self.play(
            ApplyMethod(root_highlight3.set_color, RED),
            ApplyMethod(root_highlight4.set_color, RED),
            ReplacementTransform(eq10_1.copy(),root_highlight3),
            ReplacementTransform(eq10_2.copy(),root_highlight4),
            )
        self.play(Write(root3_label),Write(root4_label))



if __name__ == "__main__":
    ###Using Python class browser to determine which classes are defined in this file
    module_name = 'quadratics1'   #Name of current file
    module_info = pyclbr.readmodule(module_name)

    for item in module_info.values():
        if item.module==module_name:
            print(item.name)
            os.system("python -m manim quadratics1.py %s -l" % item.name)  #Does not play files
