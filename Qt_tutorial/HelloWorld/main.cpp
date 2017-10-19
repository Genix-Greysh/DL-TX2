#include "mainwindow.h"
#include <QCoreApplication>
#include <QPushButton>
#include "newspaper.h"
#include "reader.h"

int main(int argc, char *argv[])
{
    // !! Qt5
    /* Singal in Qt
     * The general format:
     *     connect (sender, singal, receiver, slot)
     */

    QCoreApplication app(argc, argv);

    //QPushButton button("Quit");
    //QObject :: connect(&button, &QPushButton::clicked, &QApplication::quit);

    //button.show();
    Newspaper newspaper('Newspaper A');
    Reader reader;
    QObject :: connect(&newspaper, SIGNAL(newspaer(QString)),
                       &reader, SLOT(receivePaper(QString)));
    return app.exec();
}
