from manimlib.imports import *
import os
import pyclbr

class TeoTest(GraphScene):
    CONFIG = {
        "plane_kwargs" : {
        "x_line_frequency" : 2,
        "y_line_frequency" :2
        },
        "functions" : [lambda x: x**2 + 2*x - 1, lambda x: x**2 + 2*x+1, lambda x: x**2 + 2*x + 3],
        "color_main" : GREEN,
        "center_point" : 0,
        "x_min" : -4,
        "x_max" : 2,
        "y_min" : -2,
        "y_max" : 4,
        "graph_origin" : 2*LEFT + 1.5*DOWN,
        "x_labeled_nums" : range(-6, 4, 2),
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
        discriminant.set_color(BLUE)
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


    def construct(self):

        my_plane = NumberPlane(**self.plane_kwargs)
        my_plane.add(my_plane.get_axis_labels())
        # self.add(my_plane)
        #Show/hide grid for debugging


        self.setup_axes(animate=False)

        # self.write_eq(1,2,-2)
        eq = self.write_eq(1,2,-2)
        self.play(Write(eq))

        #retrieving these from the class attributes

        abc = self.write_abcs()

        self.play(
            Write(abc),
            ApplyMethod(eq[0].set_color, YELLOW),
            ApplyMethod(eq[3].set_color, YELLOW),
            ApplyMethod(eq[6].set_color, YELLOW),
            )

        discriminant = self.write_discriminant(self.a,self.b,self.c)

        #graphs
        graphs = [self.get_graph(f,self.color_main) for f in self.functions]

        init_graph = self.get_graph(self.functions[0], self.color_main)
        self.play(ShowCreation(init_graph))

        eq.target = self.write_eq(1,2,1)
        abc.target = self.write_abcs()
        self.play(
            MoveToTarget(eq),
            FadeOut(discriminant),
            MoveToTarget(abc),
            Transform(init_graph,self.get_graph(self.functions[1], self.color_main)),
            # ApplyMethod(eq[0].set_color, YELLOW),
            # ApplyMethod(eq[3].set_color, YELLOW),
            # ApplyMethod(eq[6].set_color, YELLOW),
            )

        #it's okay to leave write-discriminant as a self-write function
        discriminant = self.write_discriminant(self.a,self.b,self.c)









if __name__ == "__main__":
    ###Using Python class browser to determine which classes are defined in this file
    module_name = 'teo'   #Name of current file
    module_info = pyclbr.readmodule(module_name)

    for item in module_info.values():
        if item.module==module_name:
            print(item.name)
            os.system("python -m manim teo.py %s -l" % item.name)  #Does not play files
