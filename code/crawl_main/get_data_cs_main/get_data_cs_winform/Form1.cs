using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;
using System.Threading;
using System.Text.RegularExpressions;
using System.Collections;

namespace get_data_cs_winform
{
    public partial class Form1 : Form
    {
        private const int NUM_OF_COMMENTS_PAGE = 30;
        private const string DEFAULT_PATH = @"../../../../../../Data";
        private const int PAGE_AMOUNTS = 100;


        private string file_path = DEFAULT_PATH;
        private int count = 0;
        private bool isFinish = true;
        private string dir_name = "";
        private int index = 0;
        private string keyword = "";
        private string folder = "";

        private List<string> keyWords;
        private List<string> folders;

        DateTime start;
        DateTime end;
      
        private bool isBegin;

        private static string crawl_page(string url)
        {

            WebBrowser wb = new WebBrowser();
            wb.Navigate(url);
            while (true)
            {
                if (wb.DocumentText.Length > 10)
                {
                    break;
                }
            }
            return wb.DocumentText;
        }

        private void write_text(string text, string path)
        {
            using (StreamWriter sw = new StreamWriter(path))
            {
                sw.Write(text);
            }
        }
        private Hashtable GenerateStockCode()
        {
            String[] lines;
            Hashtable stockCode = new Hashtable();
            lines = File.ReadAllLines(@"stockcode.txt");
            for (int i = 0; i < lines.Length - 1; i = i + 2)
            {
                stockCode.Add(lines[i + 1], lines[i]);
            }
            return stockCode;
        }
        private void GenerateKeyWords(string fileName, List<string> folders,List<string> keyWords)
        {
            String[] lines;
            lines = File.ReadAllLines(fileName);
            for (int i = 0; i < lines.Length; i++)
            {
                folders.Add(lines[i]);
                keyWords.Add(Uri.EscapeDataString(lines[i]));
            }
        }
        
        public Form1()
        {
            InitializeComponent();
            ////////////////////////////////////////////////////////////////////////////
            start = DateTime.Now;
            ////////////////////////////////////////////////////////////////////////////
            folders = new List<string>();
            keyWords = new List<string>();
            GenerateKeyWords(@"keywordslist.txt",folders, keyWords);
            isBegin = false;
           // webBrowser1.Navigate("http://mail.sina.cn/");
        webBrowser1.Navigate("http://weibo.cn/");
        }

        private void button1_Click(object sender, EventArgs e)
        {
            dir_name = "";
            file_path = DEFAULT_PATH;

            count = 0;
            isBegin = true;

            folder = folders[index];
            keyword = keyWords[index];
            string date = "";
            DateTime dt = DateTime.Now;

            if (dt.Hour < 9)
            {
                dt = dt.AddDays(-1);
                
            }
            date = dt.ToString("yyyyMMdd");
            dir_name = this.file_path + @"\" + date;
            Directory.CreateDirectory(dir_name);
            dir_name += @"\generall";
            Directory.CreateDirectory(dir_name);
            dir_name += @"\generall_res";
            Directory.CreateDirectory(dir_name);
            dir_name += @"\" + DateTime.Now.ToString("yyyyMMddHH");
            Directory.CreateDirectory(dir_name);
            dir_name += @"\" + folder;
            Directory.CreateDirectory(dir_name);
            this.file_path = dir_name +  @"\1.html";
            webBrowser1.Navigate("http://weibo.cn/search/mblog?hideSearchFrame=&keyword=" + keyword + "&page=1");
            write_text(DateTime.Now.ToString("yyyy-MM-dd HH:mm"),dir_name+@"\basetime.txt");
        }

        private void NavigateNextPage()
        {
            int i;
            int temp = 0;
            string file_name = "";

            for (i = 2; i <= PAGE_AMOUNTS; i++)
            {
                temp = i + 1;
                file_name = string.Format(dir_name+ @"\{0}.html", i);
                if (!File.Exists(file_name))
                {
                    string comment_url = string.Format("http://weibo.cn/search/mblog?hideSearchFrame=&keyword="+keyword+"&page={0}", i);
                    if (isFinish)
                    {
                        Thread.Sleep(2000);
                        webBrowser1.Navigate(comment_url);
                        this.file_path = file_name;
                        isFinish = false;
                        return;
                    }
                }
                if (temp > PAGE_AMOUNTS)
                {
                    file_path = DEFAULT_PATH;
                    i = 1;
                    index++;
                    if (index >= folders.Count)
                    {
                        //////////////////////////////////////////////////////////////////////////
                        end = DateTime.Now;
                        TimeSpan ts = end - start;
                        double timeSpan = ts.TotalMinutes;
                        ///////////////////////////////////////////////////////////////////////
                        MessageBox.Show(timeSpan.ToString("f2"));
                        return;
                    }
                        
                    folder = folders[index];
                    
                    keyword = keyWords[index];


                    string date = "";
                    DateTime dt = DateTime.Now;

                    if (dt.Hour < 9)
                    {
                        dt = dt.AddDays(-1);
                       
                    }
                    date = dt.ToString("yyyyMMdd");
                    dir_name = this.file_path + @"\" + date;
                    Directory.CreateDirectory(dir_name);
                    dir_name += @"\generall";
                    Directory.CreateDirectory(dir_name);
                    dir_name += @"\generall_res";
                    Directory.CreateDirectory(dir_name);
                    dir_name += @"\" + DateTime.Now.ToString("yyyyMMddHH");
                    Directory.CreateDirectory(dir_name);
                    dir_name += @"\" + folder;
                    Directory.CreateDirectory(dir_name);

                    write_text(DateTime.Now.ToString("yyyy-MM-dd HH:mm"),dir_name+@"\basetime.txt");

                    file_name = string.Format(dir_name + @"\{0}.html", i);
                    if (!File.Exists(file_name))
                    {
                        string comment_url = string.Format("http://weibo.cn/search/mblog?hideSearchFrame=&keyword=" + keyword + "&page={0}", i);
                        if (isFinish)
                        {
                            Thread.Sleep(2000);
                            webBrowser1.Navigate(comment_url);
                            this.file_path = file_name;
                            isFinish = false;
                            return;
                        }
                    }
                }  
            }            
        }

        private void webBrowser1_DocumentCompleted(object sender, WebBrowserDocumentCompletedEventArgs e)
        {
            count = count - 1;

            if (0 == count && isBegin)
            {
                string html=webBrowser1.DocumentText;
                write_text(html, this.file_path);
                isFinish = true;
                NavigateNextPage();
            }

        }

        private void webBrowser1_Navigated(object sender, WebBrowserNavigatedEventArgs e)
        {
            this.count++;
        }

        private void button2_Click(object sender, EventArgs e)
        {
            folders.Clear();
            keyWords.Clear();
            GenerateKeyWords(@"keywordlisthot.txt", folders, keyWords);
            button1_Click(sender, e);
        }
    }
}
