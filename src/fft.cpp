#include <boost/python.hpp>
#include <iostream>
#include <cmath>
#include <complex>

typedef std::complex<double> cDouble;

cDouble* listToTab(boost::python::list l)
{
    int N = boost::python::len(l);
    cDouble *t = (cDouble*)c(N*sizeof(cDouble));
    for (int i=0;i<N;i++)
        t[i] = boost::python::extract<cDouble>(l[i]);
    return t;
}

cDouble** listOfListToTab(boost::python::list l)
{
    int N = boost::python::len(l);
    cDouble** t = (cDouble**)malloc(N*sizeof(cDouble*));
    for (int i=0;i<N;i++)
        t[i] = listToTab(boost::python::extract<boost::python::list>(l[i]));
    return t;
}

bool is2Power(int N) { return N==1 || (N%2==0 && is2Power(N/2)); }

int get2Power(int N) { return pow(2, ceil(log(N)/log(2))); }

cDouble e(int k, int N) { return exp((cDouble)(-2j*M_PI*k/N)); }

boost::python::list tabToList(cDouble *t, int N)
{
    boost::python::list l = boost::python::list();
    for (int i=0;i<N;i++)
        l.append(t[i]);
    return l;
}

cDouble* fftCT(cDouble *sig)
{
    int i,j,k,p=0,f=1;
    int N = 1024;
    cDouble ekN;
    cDouble **tmp = (cDouble**)malloc(2*sizeof(cDouble*));

    for (i=0;i<2;i++)
        tmp[i] = (cDouble*)malloc(N*sizeof(cDouble));
    for (i=0;i<N;i++)
        tmp[0][i] = sig[i];
    for (i=N/2;i!=1;i/=2)
    {
        for (j=0;j<i;j++)
            for (k=0;k<N/(2*i);k++)
            {
                ekN = e(k,N/i)*tmp[p][i*(2*k+1)+j];
                tmp[f][i*k+j] = tmp[p][i*(2*k)+j] + ekN;
                tmp[f][i*k+j+N/2] = tmp[p][i*(2*k)+j] - ekN;
            }
        p = f;
        f = (p+1)%2;
    }
	
	free(tmp[f]);
	
    return tmp[p];
}

cDouble* fft(cDouble *sig, int N, int *sizeC, bool mid)
{
    cDouble* C;
    if (is2Power(N)) {
        C = fftCT(sig);
    } else {
        std::cout<<"zPad needed";
        int NPadded = get2Power(N);
        cDouble* sigPadded = (cDouble*)malloc(NPadded*sizeof(cDouble));
        for (int i=0;i<N;i++)
            sigPadded[i] = sig[i];
        for (int i=N;i<NPadded;i++)
             sigPadded[i] = 0;
        C = fftCT(sigPadded);
		free(sigPadded);
    }

    if (mid) {
        int n = 512;
        cDouble *rep = (cDouble*)malloc(n*sizeof(cDouble));
        for (int i=0;i<n;i++)
            rep[i] = C[i];
        *sizeC = n;
		free(C);
        return rep;
    } else {
        *sizeC = N;
        return C;
    }
}

boost::python::list fftListe(boost::python::list pyEchs, bool mid=true)
{
    int nbEchs = boost::python::len(pyEchs);
    cDouble **echs = listOfListToTab(pyEchs);
    boost::python::list rep = boost::python::list();

    int sizeC;
    cDouble* C;
	
    for (int i=0;i<nbEchs-1;i++)
    {
        if (i%5==0) {
			std::cout<<"Traitement du " << i << "eme echantillon..." << std::endl;
		}
        C = fft(echs[i], 1024, &sizeC, mid);
        rep.append(tabToList(C, sizeC));
    }
	
    std::cout << "Traitement du dernier echantillon..." << std::endl;
    int sizeLastEch  = boost::python::len(pyEchs[nbEchs-1]);
    C = fft(echs[nbEchs-1], sizeLastEch, &sizeC, mid);
    rep.append(tabToList(C, sizeC));
	free(C);

    std::cout << "Done !" << std::endl;
    return rep;
}

BOOST_PYTHON_MODULE(fft)
{
    using namespace boost::python;
    def("fftListe", fftListe);
}

