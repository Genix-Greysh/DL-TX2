
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    return a.exec();
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
