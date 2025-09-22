#include <iostream>
#include <sstream>
#include <math.h>
#include <string>
using namespace std;
class Vehiculo{
		private :
		string marca;
		float combustible;
		float kilometraje;
		string origen;
		string destino;
		float velocidad;
public:
	Vehiculo(string _marca, float _combustible,float _kilometraje,
			 string _origen,string _destino,float _velocidad){
		this->marca=_marca;
		this->combustible= _combustible;
		this->kilometraje=_kilometraje;
		this->origen=_origen;
		this->destino=_destino;
		this->velocidad=_velocidad;
	}
	Vehiculo(){
		this->marca="Indeterminado";
		this->combustible= 0;
		this->kilometraje=0;
		this->origen="Fabrica";
		this->destino="Indeterminado";
		this->velocidad=0;
	}
		Vehiculo(string _marca, float _kilometraje){
			this->marca= _marca;
			this->combustible= 0;
			this->kilometraje=_kilometraje;
			this->origen="Fabrica";
			this->destino="Indeterminado";
			this->velocidad=0;
		}
	
	string getMarca(){
		return marca;
	}
	void setMarca(string _marca){
			marca= _marca;
	}
	float getLitro(){
	return combustible;
	}
	void setLitro(float _combustible){
	combustible = _combustible;
	}		
	float getKilometraje (  )
	{   return( kilometraje );}
	void  setKilometraje ( float _kilometraje )
	{        kilometraje = _kilometraje;}
	
	string getOrigen ( )
	{  return ( origen );}
	void setOrigen ( string _origen )
	{        origen = _origen;}
	
	string getDestino ( )
	{    return destino ;}
	void setDestino ( string _destino )
	{        destino = _destino;}
	
	float getVelocidad (  )
	{    return ( velocidad );}
	void setVelocidad ( float _velocidad )
	{        velocidad = _velocidad;}
	//Metodos
	float  rendimientoPromedio ( ) {
		return ( combustible  / kilometraje );
	}
	void aumentaCombustible (float litros) {
		combustible = combustible + litros;
		cout<<"EL aumento de combustible que se debe hacer es de:"<<combustible<<endl;
	
	}
	
	string toString(){
		stringstream s;
		s <<"El automovil es de marca:"<<" "<< this->marca<<endl;
		s <<"El combustible en el tanque es de:"<<" "<< this-> combustible <<"L"<<endl;
		s <<"El kilometraje recorrido es de:" <<" "<< this-> kilometraje <<"Km"<<endl;
		s <<"Cuidad de Origen:" <<" "<< this-> origen<<endl;
		s <<"Cuidad Destino:"<<" "<< this-> destino<<endl;
		s <<"Velocidad:"<<" "<< this-> velocidad<<"Km/h"<<endl;
		return s.str();
	}
			
			
			
			
			
			
		~Vehiculo(){
			
		}		
};		
			
int main(int argc, char *argv[]) {
	string marca;
	float combustible;
	float kilometraje;
	string origen;
	string destino;
	float velocidad;
	cout<<"Bienvenido a MecanicFF a tu alcance"<<endl;
	cout<<"Digite los datos del primer vehiculo : "<<endl;
	cout<<"Digite la marca : ";
	cin>>marca;
	cout<<"Cantidad de gasolina? ";
	cin>>combustible;	
	cout<<"Kilometraje recorrido? ";
	cin>>kilometraje;
	cin.ignore();
	cout << "Ingrese el nombre de la ciudad de origen: ";
	getline(cin, origen);
	cout << "Ingrese el nombre de la ciudad destino: ";
	getline(cin, destino);
	cout<<"velocidad? "<<endl;
	cin>>velocidad;
	Vehiculo v1(marca,combustible,kilometraje,origen,destino,velocidad);
	cout<<"Datos del primer vehiculo"<<endl;
	
	cout<<v1.toString()<<endl;
	
	cout<<"El rendimiento promedio del Vehiculo es:"<<v1.rendimientoPromedio()<<endl;
	v1.aumentaCombustible(10.0);cout<<"L";
	system("pause");	
	
	
	
	
	cout<<"Datos del segundo vehiculo"<<endl;
	Vehiculo v2("Toyota",50,3000,"Japón","UNA",150);
	cout << "El segundo vehiculo es de marca: " << v2.getMarca() << endl;
	v2.setMarca("RAM");
	cout<<v2.getMarca()<<endl;
	cout<<v2.toString()<<endl;
	cout<<"El rendimiento promedio del Vehiculo es:"<<v2.rendimientoPromedio()<<endl;
	v2.aumentaCombustible(10);cout<<"L";
	system("pause");
	cout<<"Datos del tercer vehiculo"<<endl;
	Vehiculo v3("lamborghini",80,5000,"Rusia","Rumania",100);
	cout << "El tercer vehiculo es de marca: " << v3.getMarca() << endl;
	cout<<"Debido a un error la marca no es la correcta si no la siguiente :";
	v3.setMarca("Toyota");
	cout<<v3.getMarca()<<endl;
	cout<<"Debido a un error de datos el origen del Vehiculo es incorrecto"<<endl;
	cout<<"Por lo tanto el origen correcto del Vehiculo es el siguiente:"<<endl;
	v3.setOrigen("America Central");
	cout<<v3.getOrigen()<<endl;
	cout<<"Debido a un error de datos el destino del Vehiculo es incorrecto"<<endl;
	cout<<"Por lo tanto el destino correcto del Vehiculo es el siguiente:"<<endl;
	v3.setDestino("Corea");
	cout<<v3.getDestino()<<endl;
	cout<<"Debido a un error de datos el kilometraje del Vehiculo es incorrecto"<<endl;
	cout<<"Por lo tanto el kilometraje correcto del Vehiculo es el siguiente:"<<endl;
	v3.setKilometraje(5230);
	cout<<v3.getKilometraje()<<endl;
	cout<<"Debido a un error de datos la velocidad del Vehiculo es incorrecto"<<endl;
	cout<<"Por lo tanto la velocidad correcto del Vehiculo es el siguiente:"<<endl;
	v3.setVelocidad(20);
	cout<<v3.getVelocidad()<<endl;
	cout<<v3.toString()<<endl;
	cout<<"El rendimiento promedio del Vehiculo es:"<<v3.rendimientoPromedio()<<endl;
	v3.aumentaCombustible(10);cout<<"L";
	system("pause");
		
		
		
		
		
		
		
		
		
		
		
	return 0;
	}
