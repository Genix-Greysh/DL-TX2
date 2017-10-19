#ifndef NEWSPAPER_H
#define NEWSPAPER_H

class Newspaper : public QObject
{
    Q_OBJECT
public :
    Newspaper(const QString & name) :
        m_name(name)
    {

    }

    void send()
    {
        emit newPaper(m_name);
    }

    signals:
        void newPaper(const QString &name) const;

     private:
        QString m_name;

}; 

#endif // NEWSPAPER_H
