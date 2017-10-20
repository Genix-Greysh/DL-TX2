#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <QDebug>
#include <QDir>
#include <QApplication>

using namespace std;
using namespace cv;

int face_demo(CascadeClassifier& ccf);
void detector(Mat& img, Mat& colorImg, CascadeClassifier& ccf);

int main()
{

    char*  xmlPath = "haarcascade_frontalface_default.xml";
    CascadeClassifier ccf;
    Mat img = imread("psb2.jpeg", 0 );
    Mat colorImg = imread("psb2.jpeg");
    imshow("hello", img);
    waitKey(0);
    //cvtColor(colorImg, colorImg, CV_BGR2GRAY);
    if(!ccf.load(xmlPath))
    {
        cout<<"不能加载指定的xml文件"<<endl;
        return 0;
    }

    face_demo(ccf);
    waitKey(0);
    return 1;
}

int face_demo(CascadeClassifier& ccf)
{
     VideoCapture cap(0);
     if(!cap.isOpened())
     {
         return -1;
     }

     Mat frame;
     Mat grayframe;
     bool stop = false;
     int delay = 30;

     while(!stop)
     {
         cap>>frame;
         grayframe = frame;

         cvtColor(grayframe, grayframe, CV_BGR2GRAY);
         detector(grayframe, frame, ccf);

         if(waitKey(delay) >=0 && delay >=0)
             stop = true;
     }
     return 0;
}


void detector(Mat& img, Mat& colorImg, CascadeClassifier& ccf)
{
    vector<Rect> faces;  //创建一个容器保存检测出来的脸
    Mat gray;


    gray = img;
    equalizeHist(gray,gray);  //直方图均衡行

    ccf.detectMultiScale(gray, faces, 1.1, 3, 0, Size(10,10), Size(100,100)); //检测人脸
    for(vector<Rect>::const_iterator iter = faces.begin(); iter != faces.end(); iter++)
    {
        rectangle(colorImg,*iter,Scalar(0,0,255),2,8); //画出脸部矩形
    }
    imshow("faces", colorImg);
}

