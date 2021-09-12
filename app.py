from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('home.html')


@app.route('/resultado', methods=['POST'])
def calcular():
    if request.method == 'POST':
        
        
        voltaje_bateria=int(request.form.get('voltaje'))
        amperios_bateria=int(request.form.get('amperios'))
        array = request.form.getlist('field[]')
        #Variables
        consumo_promeido_diario=0
        watts_totales=0
        amperes_hora_dia=0
        amperes_pico=0
        baterias_serie=0
        baterias_paralelo=0
        baterias_totales=0
        modulos_serie=0
        modulos_paralelo=0
        modulos_totales=0
        array=list(map(float, array))
          
        
        for i in range(0,len(array),4):
            consumo_promeido_diario+=array[i]*array[i+1]*array[i+2]*array[i+3]/7
            watts_totales+=array[i+1]
        
        #Dimensionado de baterias
        amperes_hora_dia=consumo_promeido_diario/0.9/48
        baterias_paralelo=round(amperes_hora_dia*4/0.5/amperios_bateria)
        baterias_serie=round(48/voltaje_bateria)
        baterias_totales=baterias_paralelo*baterias_serie

        #Dimensionado del sistema
        amperes_pico=amperes_hora_dia/0.8/4
        #Numero de modulos fotovoltaicos
        modulos_paralelo=round(amperes_pico/5)
        modulos_serie=48/12
        modulos_totales=modulos_paralelo*modulos_serie

        respuesta={
            "consumo_diario":round(consumo_promeido_diario),
            "watts_totales":watts_totales,
            "amperes_hora_dia":round(amperes_hora_dia,2),
            "amperes_pico_arreglo":round(amperes_pico,2),
            "baterias_serie":baterias_serie,
            "baterias_paralelo":baterias_paralelo,
            "baterias_totales":baterias_totales,
            "capacidad_bateria":amperios_bateria,
            "voltaje_bateria":voltaje_bateria,
            "modulos_serie":int(modulos_serie),
            "modulos_paralelo":int(modulos_paralelo),
            "modulos_totales":int(modulos_totales),

        }
        
        return render_template('result.html', rs=respuesta)

       


if __name__ == ' __main__':
    app.debug = True
    app.run()
