using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Threading;
using System.Net.Sockets;
using System.Net;
using System.IO;

namespace Vis
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public int width = 1;
        public int height = 1;
        public int pixelSize = 6;
        public List<Rectangle> pixels;
        private Canvas cvs = null;
        private RenderTargetBitmap rtb = null;
        private int draw_width = 1;
        private int draw_height = 1;
        private int count = 0;

        public List<Rectangle> setupGrid(int width, int height)
        {
            this.cvs = new Canvas();
            this.cvs.Width = this.draw_width = (this.pixelSize * this.width) + this.width - 1;
            this.cvs.Height = this.draw_height = (this.pixelSize * this.height) + this.height - 1;
            this.cvs.Background = new SolidColorBrush(Colors.Black);

            this.rtb = new RenderTargetBitmap(this.draw_width, this.draw_height,
                                              96, 96, PixelFormats.Pbgra32);

            var xPos = 0;
            var yPos = 0;

            var results = new List<Rectangle>();
            var fill = new SolidColorBrush(Color.FromRgb(42, 42, 42));
            for (int y = 0; y < this.height; y++)
            {
                for (int x = 0; x < this.width; x++)
                {
                    var r = new Rectangle();
                    r.Width = r.Height = this.pixelSize;
                    r.StrokeThickness = 0;
                    r.Fill = fill;
                    cvs.Children.Add(r);
                    Canvas.SetTop(r, yPos);
                    Canvas.SetLeft(r, xPos);
                    results.Add(r);

                    xPos += this.pixelSize + 1;
                }

                xPos = 0;
                yPos += this.pixelSize + 1;
            }

            this.draw_grid();
            return results;
        }

        public void update(byte[] data)
        {
            this.Dispatcher.Invoke(DispatcherPriority.Render,
                (ThreadStart)delegate ()
                {
                    var dPos = 0;
                    if (data.Length != this.pixels.Count * 3)
                    {
                        Console.WriteLine("Invalid pixel count!");
                    }
                    else
                    {
                        var black = Color.FromRgb(0, 0, 0);
                        foreach (var r in this.pixels)
                        {
                            var c = Color.FromRgb(data[dPos + 0], data[dPos + 1], data[dPos + 2]);
                            if(c == black)
                            {
                                Console.WriteLine("Black: " + dPos);
                                break;
                            }
                            r.Fill = new SolidColorBrush(c);
                            dPos += 3;
                        }
                    }
                    
                    this.draw_grid();
                }
                );
        }

        public void draw_grid()
        {
            var size = new Size(this.draw_width, this.draw_height);
            this.cvs.Measure(size);
            this.cvs.Arrange(new Rect(size));
            this.rtb.Render(this.cvs);
            PngBitmapEncoder encoder = new PngBitmapEncoder();
            encoder.Frames.Add(BitmapFrame.Create(this.rtb));

            using (FileStream file = File.Create(this.count + ".png"))
            {
                encoder.Save(file);
            }
            this.count++;

            this.Content = new Image { Source = this.rtb, Width = this.draw_width, Height = this.draw_height };
        }

        public MainWindow()
        {
            InitializeComponent();
            string[] args = Environment.GetCommandLineArgs();
            if(args.Length != 3)
            {
                MessageBox.Show("Must provide width and height! vis.exe <width> <height>");
                Application.Current.Shutdown();
            }

            this.width = int.Parse(args[1]);
            this.height = int.Parse(args[2]);   

            this.pixels = setupGrid(int.Parse(args[1]), int.Parse(args[2]));
        }
        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            CreateServer(width * height * 3);
        }

        private void CreateServer(int size)
        {
            int dataSize = size;
            size += 3; //for header
            var tcp = new TcpListener(IPAddress.Any, 1618);
            tcp.Start();

            var listeningThread = new Thread(() =>
            {
                while (true)
                {
                    var tcpClient = tcp.AcceptTcpClient();
                    NetworkStream stream = tcpClient.GetStream();
                    var data = new List<byte>();
                    int s = 0;

                    byte[] cmd = new byte[1];
                    byte[] dSize = new byte[2];
                    stream.Read(cmd, 0, 1);
                    stream.Read(dSize, 0, 2);

                    s = dSize[0] + (dSize[1] << 8);

                    //Console.WriteLine(cmd[0] + " - " + s);

                    if (s > 0)
                    {
                        byte[] buf = new byte[s];

                        while (data.Count < s)
                        {
                            int i = stream.Read(buf, 0, s);
                            //Console.WriteLine(i);
                            data.AddRange(buf);
                        }

                        if (data.Count == dataSize)
                        {
                            if(cmd[0] == 2)
                            {
                                this.update(data.ToArray());
                            }
                            

                        }
                        else
                        {
                            Console.WriteLine("Received " + data.Count + " bytes, but " + dataSize + " expected.");
                        }
                    }
                    

                    tcpClient.GetStream().WriteByte(255);
                    tcpClient.GetStream().Flush();
                    tcpClient.Client.Shutdown(SocketShutdown.Both);
                    //tcpClient.GetStream().Close();
                    //tcpClient.Close();
                    //while (tcpClient.Connected) { Thread.Sleep(1); }
                    //Thread.Sleep(500);
                }
            });

            listeningThread.IsBackground = true;
            listeningThread.Start();
        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            //this.srv.Stop();
        }
    }
}
