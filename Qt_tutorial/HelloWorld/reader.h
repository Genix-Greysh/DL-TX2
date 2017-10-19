#ifndef READER_H
#define READER_H
#include <QObject>
#include <QDebug>

class Reader : public QObject
{
    Q_OBJECT
public :
    Reader() {}

public slots:
    void receiveNewspaper(const QString &name) const
    {
        qDebug() << "Recevie Newspaper: " << name;
    }
};

#endif // READER_H
