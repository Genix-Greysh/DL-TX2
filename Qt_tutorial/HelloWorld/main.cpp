#include "mainwindow.h"
#include <QApplication>
#include <QPushButton>

int main(int argc, char *argv[])
{
    // !! Qt5
    /* Singal in Qt
     * The general format:
     *     connect (sender, singal, receiver, slot)
     */

    QApplication app(argc, argv);

    QPushButton button("Quit");
    QObject :: connect(&button, &QPushButton::clicked, &QApplication::quit);

    button.show();
    return app.exec();
}
