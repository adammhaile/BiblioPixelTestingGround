using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using OpenTK;
using OpenTK.Graphics.OpenGL;


namespace GLVis
{
    class Main : GameWindow
    {
        public Main()// : base (800, 600)
        {
            Title = "GLVis";
            Width = 640;
            Height = 480;
        }

        protected override void OnLoad(EventArgs e)
        {
            base.OnLoad(e);

            //This is the base color of are renderer
            //this color will fill the buffer after clearing it in OnRenderFrame
            GL.ClearColor(0.0f, 0.0f, 0.0f, 0.0f);
        }

        protected override void OnResize(EventArgs e)
        {
            base.OnResize(e);

            //Setting up a viewport using the native windows Width and Height
            //you can have multiple viewports for splitscreen but for now just one.
            GL.Viewport(0, 0, Width, Height);

            //Get the aspect ratio of the screen
            double aspect_ratio = Width / (double)Height;
            //Field of view of are camera
            float fov = 1.0f;
            //The nearest the camera can see, want to keep this number >= 0.1f else visible clipping ensues
            float near_distance = 1.0f;
            //The farthest the camera can see, depending on how far you want to draw this can be up to float.MaxValue
            float far_distance = 1000.0f;

            //Now we pass the parameters onto are matrix
            OpenTK.Matrix4 perspective_matrix =
               OpenTK.Matrix4.CreatePerspectiveFieldOfView(fov, (float)aspect_ratio, near_distance, far_distance);

            //Then we tell GL to use are matrix as the new Projection matrix.
            GL.MatrixMode(MatrixMode.Modelview);
            GL.LoadMatrix(ref perspective_matrix);
        }

        protected override void OnUpdateFrame(FrameEventArgs e)
        {
            base.OnUpdateFrame(e);
        }

        protected override void OnRenderFrame(FrameEventArgs e)
        {
            base.OnRenderFrame(e);

            //Clear the current buffers
            GL.Clear(ClearBufferMask.ColorBufferBit | ClearBufferMask.DepthBufferBit);

            //Swap to the modelview so we can draw all of are objects
            GL.MatrixMode(MatrixMode.Modelview);
            GL.LoadIdentity();

            //Now we draw something fancy... a quad
            //before that we have to set the coords they are currently (0, 0, 0) and are object
            //will not be visible to us.
            GL.Translate(0, 0, -5);

            //Set the current color to red in this case
            GL.Color3(System.Drawing.Color.Red);

            //Tell GL that we are going to start drawing
            GL.Begin(PrimitiveType.Quads);
            //now we setup the vertices in counter clockwise order since that
            //is GL's default.
            //GL.Vertex2(1, 1);
            //GL.Vertex2(-1, 1);
            //GL.Vertex2(-1, -1);
            //GL.Vertex2(1, -1);
            GL.Color3(System.Drawing.Color.Red);
            GL.Vertex2(0, 0);
            GL.Color3(System.Drawing.Color.Green);
            GL.Vertex2(0, 2);
            GL.Color3(System.Drawing.Color.Blue);
            GL.Vertex2(2, 2);
            GL.Color3(System.Drawing.Color.White);
            GL.Vertex2(2, 0);
            
            GL.End();

            //Present to the front buffer
            SwapBuffers();
        }
    }
}
