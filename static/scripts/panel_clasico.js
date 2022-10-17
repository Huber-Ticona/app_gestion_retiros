

function handler(e) {
    //alert(e.target.value);
    let nueva_fecha = e.target.value
    cargar_body(nueva_fecha)
    
}
/*function cargar_body(x_fecha){ MULTIUSO, ENTRE PANEL CLASICO Y INFORMES
    $('#titulo_panel').text("Panel clasico del " + x_fecha)
    $('#body_panel').load("/obtener/docs/"+ x_fecha);
}*/

function ver_bol_fact(interno,tipo_doc,folio,monto_total,vendedor,revisor,fecha){ 
    $('.modal-header').empty()
    $('.modal-body').empty()          
    $('.modal-footer').empty()
    
    $.ajax({
        url: "/obt_detalle_bol_fact/" + interno,
        type: "POST",
        success: function(resp){
            console.log(resp)
            respuesta = resp
            
            a = '<div class="row"><div class="col col-sm"><table id="table_info1"><thead><td>'
            b = 'DESCRIPCIÓN</td><td>CANTIDAD</td><td>CANTIDAD RETIRADA</td></thead></table></div></div>'
            items_lista = buscar_adj(tipo_doc,folio)
            //ADJUNTOS
            c = '<div class="text-center">Documentos Adjuntos <span class="badge badge-info"> '+items_lista[1].toString()+'</span> <button class="btn btn-secondary" onclick="ver_adjuntos()">Ver</button><div class="list-group" id= "lista_adjuntos" style="display:None;">'
            d ='</div>'
            e = ''
            f = ''
            g = ''
            if(tipo_usuario == 'porteria'){
                e='<div class="input-group" style="margin-top:10px;"><div class="custom-file"><input type="file" accept="image/*" class="custom-file-input" id="archivo" required><label class="custom-file-label" for="nombre_archivo">'
                f ='Elegir o Tomar Foto</label></div><div class="input-group-append"><button class="btn btn-outline-secondary" type="button"'
                g ='onclick = adjuntar('+folio+','+'"'+ tipo_doc +'"'+','+interno+') >Adjuntar</button></div></div>'
            } //VINCULOS
            vinculos = buscar_vinc(tipo_doc,folio)
            v = ''
            nro_vinc = 0
            if(vinculos){
                vinculos = vinculos[1]
                if(vinculos.ordenes){
                    console.log('tiene ordenes')
                    v = v + visualizar_vinc_ordenes(vinculos)  
                    nro_vinc = nro_vinc + 1
                }
                if(vinculos.guias){
                    console.log('tiene guias')
                    dguia =  '<li class="list-group-item">GUIAS: '
                    for(let p = 0; p < vinculos.guias.length ; p ++){
                        dguia = dguia + '<a href="/documentos/guias/'+(vinculos.guias[p]).toString() +'"  class="myButton2" >'+ (vinculos.guias[p]).toString() +'</a>'
                    }
                    dguia = dguia + '</li>'
                    v = v + dguia
                    nro_vinc = nro_vinc + 1
                }
                if(vinculos.creditos){
                    console.log('tiene creditos')
                    dcredito =  '<li class="list-group-item">CREDITOS: '
                    for(let p = 0; p < vinculos.creditos.length ; p ++){
                        dcredito = dcredito + '<a href="/documentos/creditos/'+(vinculos.creditos[p]).toString() +'"  class="myButton2" >'+ (vinculos.creditos[p]).toString() +'</a>'
                    }
                    dcredito = dcredito + '</li>'
                    v = v + dcredito
                    nro_vinc = nro_vinc + 1
                }
            }
            h = '<div class="text-center">Vinculos <span class="badge badge-info">'+nro_vinc.toString() +'</span> <button class="btn btn-secondary" onclick="ver_vinculos()"> Ver </button><ul class="list-group" id= "lista_vinculos" style="display: None;">'
            k = '</ul></div>'
            items_historial = buscar_historial(tipo_doc,folio)
            y = '<div >Historial de retiros <span class="badge badge-info">'+(items_historial[1]).toString() +'</span> <button class="btn btn-secondary" onclick="ver_historial()"> Ver </button><ul class="list-group" id= "lista_historial" style="display: None;">'
            z = '</ul></div>'
            $('.modal-body').append(a + b + c+ items_lista[0] + d + e+ f +g + h + v + k + y + items_historial[0] +z)

            for( i = 0 ; i < resp.length ; i++ ){
                //console.log(resp[i][2])//items retirados
                desc = resp[i][0]
                maxim = resp[i][1]
                if(resp[i][2]){
                    ret = resp[i][2]
                }else{
                    ret = "0"
                }
                //console.log(ret)
                fila = (i+1).toString()
                
                ab = '<tr><td>'+desc+'</td><td id="item_max_'+fila+'">'+maxim+'</td><td><button type="button" class="btn btn-light" onclick=reducir('+fila+','+ret+') >-</button>'
                cd = '<input class= "myinput" type="number" id="item_ret_'+fila+'" value="'+ ret +'"><button type="button" class="btn btn-light" onclick=aumentar('+fila+','+maxim+') >+</button></td></tr>'
                $('#table_info1').append( ab + cd )
            }
            
            l = '<div><h4>Vendedor: '+ vendedor + '</h4><h4>Revisor: '+ revisor + '</h4></div>'
            m = ''
            if(tipo_usuario == 'porteria'){
                //console.log('usuario de prteria detectado')
                m = '<button class="btn btn-secondary" onclick=guardar_cambios("'+ tipo_doc+'","'+ folio +'") >Guardar Cambios</button>'
            }  
            $('.modal-footer').append(l + m)

        }
    })
    //
    
    h1 = '<div id="left-header"><h4 class="modal-title">'+  tipo_doc +': ' + folio+'  |  Total: $' +monto_total+' '+'</h4></div>'
    h2 = ''
    if(tipo_usuario == 'porteria'){
        h2 = '<button class="btn btn-secondary" style="margin-left:5px;" onclick= dar_baja()>Dar de Baja</button>' }
    h3 ='<button type="button" class="close" data-dismiss="modal">&times;</button>'
    $('.modal-header').append(h1 + h2 + h3)
    aux_fecha = obtener_fecha(fecha)
    $('#left-header').append('<h4>Fecha: '+ aux_fecha +'</h4>') 
    
    $('#modal_info').modal('show')// SE MUESTRA EL MODAL
}
function ver_guia(interno,tipo_doc,folio,monto_total,vendedor){ 
    $('.modal-header').empty()
    $('.modal-body').empty()          
    $('.modal-footer').empty()
    $.ajax({
        url: "/obt_detalle_guia/" + interno,
        type: "POST",
        success: function(resp){
            //console.log(resp)
            respuesta = resp
            detalle = JSON.parse(resp[0])
            console.log(detalle) 
            adj = JSON.parse(resp[1])
            vinc = JSON.parse(resp[2])
            aux_fecha = obtener_fecha(resp[3]) 
            $('#left-header').append('<h4>Fecha: '+ aux_fecha +'</h4>')            
            a = '<div class="row"><div class="col col-sm"><table id="table_info1"><thead><td>'
            b = 'DESCRIPCIÓN</td><td>CANTIDAD</td><td>CANTIDAD RETIRADA</td></thead></table></div></div>'

            items_lista = ''
            nro_adj = 0
            if(adj != null){
                for(let j = 0; j < adj.length ; j++ ){
                items_lista = items_lista + '<a href="/descargar/'+adj[j]+'">'+'<button type="button" class="list-group-item list-group-item-action">'+ adj[0] + '</button></a>'
                nro_adj = nro_adj + 1
            }
            }
            //ADJUNTOS
            c = '<div class="text-center">Documentos Adjuntos <span class="badge badge-info"> '+nro_adj.toString()+'</span> <button class="btn btn-secondary" onclick="ver_adjuntos()">Ver</button><div class="list-group" id= "lista_adjuntos" style="display:None;">'
            d ='</div>'
            e = ''
            f = ''
            g = ''
            if(tipo_usuario == 'porteria'){
                e='<div class="input-group" style="margin-top:10px;"><div class="custom-file"><input type="file" accept="image/*" class="custom-file-input" id="archivo" required><label class="custom-file-label" for="nombre_archivo">'
                f ='Elegir o Tomar Foto</label></div><div class="input-group-append"><button class="btn btn-outline-secondary" type="button"'
                g ='onclick = adjuntar('+folio+','+'"'+ tipo_doc +'"'+','+interno+') >Adjuntar</button></div></div>'
            }
            //VINCULOS
            nro_vinc = 0 //SE ESTABLECE 0 LA CANTIDAD DE VINCULOS
            i = ''
            if(detalle.tipo_doc == 'FACTURA'){
                i =  '<li class="list-group-item">FACTURA: <a href="/documentos/facturas/'+(detalle.doc_ref).toString() +'"  class="myButton2" >'+(detalle.doc_ref).toString() +'</a></li>'
                nro_vinc = 1
            }
            else if(detalle.tipo_doc == 'BOLETA'){
                i =  '<li class="list-group-item">BOLETA: <a href="/documentos/boletas/'+(detalle.doc_ref).toString() +'"  class="myButton2" >'+(detalle.doc_ref).toString() +'</a></li>'
                nro_vinc = 1
            }
            if(vinc){
                nro_vinc = nro_vinc + 1
                i = i + visualizar_vinc_ordenes(vinc)
            }
            

            h = '<div class="text-center">Vinculos <span class="badge badge-info">'+nro_vinc.toString()+'</span> <button class="btn btn-secondary" onclick="ver_vinculos()"> Ver </button><ul class="list-group" id= "lista_vinculos" style="display: None;">'
            k =  '</ul></div>'
            items_historial = buscar_historial('GUIA',folio)
            y = '<div >Historial de retiros <span class="badge badge-info">'+(items_historial[1]).toString() +'</span> <button class="btn btn-secondary" onclick="ver_historial()"> Ver </button><ul class="list-group" id= "lista_historial" style="display: None;">'
            z = '</ul></div>'
            $('.modal-body').append(a + b + c + items_lista + d + e+ f +g + h + i + k + y + items_historial[0] + z)

            cantidades = detalle.cantidades
            descripciones = detalle.descripciones
            retirados = detalle.retirado
            revisor = detalle.revisor
            //console.log(retirados)
            for( i = 0 ; i < cantidades.length ; i++ ){
                //console.log(resp[i][2])//items retirados
                desc = descripciones[i]
                maxim = cantidades[i]
                if(retirados){
                    console.log("existe cantidad retirada")
                    ret = retirados[i]
                }else{ 
                    console.log("no existe retirado")
                    ret = "0" 
                }
                fila = (i+1).toString()
                
                ab = '<tr><td>'+desc+'</td><td id="item_max_'+fila+'">'+maxim+'</td><td><button type="button" class="btn btn-light" onclick=reducir('+fila+','+ret+') >-</button>'
                cd = '<input class= "myinput" type="number" id="item_ret_'+fila+'" value="'+ ret +'"><button type="button" class="btn btn-light" onclick=aumentar('+fila+','+maxim+') >+</button></td></tr>'
                //    <span id="item_ret_'+fila+'">  '+ret+'</span>
                $('#table_info1').append( ab + cd )
            }
            
            l = '<div><h4>Vendedor: '+ vendedor + '</h4><h4>Revisor: '+ revisor + '</h4></div>'
            m = ''
            if(tipo_usuario == 'porteria'){
                m = '<button class="btn btn-secondary" onclick=guardar_cambios_2('+ interno.toString()+') >Guardar Cambios</button>'
            }
            $('.modal-footer').append(l + m)

        }
    })
    //
    
    h1 = '<div id="left-header"><h4 class="modal-title">'+  tipo_doc +': ' + folio+'  |  Total: $' +monto_total+' '+'</h4></div>'
    h2 = ''
    if(tipo_usuario == 'porteria'){
        h2 = '<button class="btn btn-secondary" style="margin-left:5px;" onclick= dar_baja()>Dar de Baja</button>' }
    h3 ='<button type="button" class="close" data-dismiss="modal">&times;</button>'
    $('.modal-header').append(h1 + h2 + h3)
    $('#modal_info').modal('show')// SE MUESTRA EL MODAL
}
function visualizar_vinc_ordenes(detalle){
    console.log(detalle)
    console.log(detalle.ordenes)
    cadena = '<li class="list-group-item">ORDEN DE TRABAJO: '
    console.log('analizando vinc a ordenes')
    for(let k = 0; k < (detalle.ordenes).length ; k ++){
        orden = JSON.parse(detalle.ordenes[k])
        console.log(orden)
        if(orden.tipo == 'dimensionado'){
            aux = 'DIM'
        }
        else if(orden.tipo == 'elaboracion'){
            aux = 'ELAB'
        }
        else if(orden.tipo == 'carpinteria'){
            aux = 'CARP'
        }
        else if(orden.tipo == 'pallets'){
            aux = 'PALL'
        }
        cadena = cadena +  '<a href="/documentos/ordenes/'+ aux.toLowerCase() +'/'+(orden.folio).toString() +'"  class="myButton2" >'+ aux + ' '+(orden.folio).toString() +'</a>'
    }
    cadena = cadena + '</li>'
    //console.log(cadena)
    return cadena
}

function buscar_adj(tipo,folio){
    console.log('buscando adjuntos ...')
    let found = []
    if(tipo== "BOLETA"){
        found = lista_bol_adj.find(element => element[0] == folio )
    }
    else if(tipo=="FACTURA"){
         found = lista_fact_adj.find(element => element[0] == folio )
    }

    items_lista = ""
    nro_adj = 0
    if(found[1] != null){
        lista = found[1]
        for(let i = 0 ; i < lista.length ; i++){
            items_lista = items_lista + '<a href="/descargar/'+lista[i]+'">'+'<button type="button" class="list-group-item list-group-item-action">'+ lista[i] + '</button></a>'
            nro_adj = nro_adj + 1
    }
    }else{
        console.log('Adjunto no encontrado')
    }    
    return [items_lista, nro_adj ]
}

function buscar_vinc(tipo,folio){
    console.log('buscando vinculos...')
    let found2 = []
    if(tipo== "BOLETA"){
        found2 = lista_bol_vinc.find(element => element[0] == folio )
        
    }
    else if(tipo=="FACTURA"){
         found2 = lista_fact_vinc.find(element => element[0] == folio )
        }
    if(found2 != null){
        console.log(found2)
    }else{
        console.log('vinculos no encontrados')
    }
    return found2
}
function aumentar(fila,max){
    // max: hace referencia a la cantidad maxima que se puede retirar. En este caso la cantidad total de items comprados.
    ret = $('#item_ret_'+fila).val()
    
    cant = parseInt(ret) + 1
    if(cant <= max){
        $('#item_ret_'+fila).val(cant)
    }else{
        alert('No puede retirar más de lo comprado.')
    }
}
function reducir(fila,min){
    // min: hace referencia a la ultima cantidad retirada que se registro en el sistema.
    ret = $('#item_ret_'+fila).val()
    
    cant = parseInt(ret)  - 1
    if(cant >= 0){
        $('#item_ret_'+fila).val(cant)
    }else{
        alert('No puede retirar menos de 0.')
    }
}
function dar_baja(){
    var tabla = document.getElementById('table_info1')
    for (var i = 1, row; row = tabla.rows[i]; i++) {
        maximo = row.cells[1].innerText
        maximo = parseFloat(maximo)
        $('#item_ret_'+i.toString()).val(maximo)
        //retirada = $('#item_ret_'+ i.toString()).text()
        //console.log(retirada)
    }
    /*console.log(lista_bol_vinc)
    console.log(lista_fact_vinc)
    console.log(lista_bol_adj)
    console.log(lista_fact_adj) */ 

}
function guardar_cambios(tipo_doc,folio){ //ACTUALIZAR BOLETA O FACTURA
    var tabla = document.getElementById('table_info1')
    datos = []
    estado = true // checkea si se actualiza el documento o no.
    estado_retiro = 'NO RETIRADO'
    total_retirada = 0
    total_comprada = 0
    total_ret_anterior = 0
    interno = respuesta[0][4]

    l_descripciones = []
    l_retirado = []
    l_ret_anterior = []
    
    for (var i = 1, row; row = tabla.rows[i]; i++) {
        item = []
        comprada = $('#item_max_'+ i.toString()).text()
        retirada = $('#item_ret_'+ i.toString()).val()
        
        ret_anterior = respuesta[i - 1][2]
        if(ret_anterior == null){
            ret_anterior = 0
        }
        if(retirada == ''){
            console.log('item vacio')
            estado = false
            retirada = 0
        }
        console.log("Fila: "+comprada + " - " + retirada + ' - anterior: ' + ret_anterior.toString())
        
        comprada = parseFloat(comprada)
        retirada = parseFloat(retirada)
        
        if(retirada > comprada){
            estado = false
        }
        if(retirada < 0){
            estado = false
        }
        total_ret_anterior = total_ret_anterior + ret_anterior
        total_retirada = total_retirada + retirada
        total_comprada = total_comprada + comprada
        cod = respuesta[i - 1][3]
        
        item.push(retirada)
        item.push(cod) 
        item.push(interno)
        datos.push(item)
        //historial
        l_descripciones.push(respuesta[i -1][0])
        l_ret_anterior.push( ret_anterior )
        l_retirado.push( parseFloat(retirada) )
        
    }
    console.log('TOTAL COMPRADA: ' + total_comprada.toString())
    console.log('TOTAL retirada actual: ' + total_retirada.toString())
    console.log('TOTAL ret ANTERIOR: ' + total_ret_anterior.toString())
    //console.log(datos)
    console.log(l_descripciones)
    console.log(l_ret_anterior)
    console.log(l_retirado)

    if(estado == false){
        alert('Un item supera la cantidad comprada, tiene un valor negativo o un campo esta incompleto')
        console.log('Un item supera la cantidad comprada o tiene un valor negativo')
    }
    else if(total_retirada > total_comprada){
        estado = false //no puede modificar el documento
        alert('No puede retirar mas de lo comprado')
        console.log('no puede retirar mas de lo comprado')
    }
    else if(total_retirada < 0 ){
        estado = false //no puede modificar el documento
        alert('No puede retirar cantidades negativas')
        console.log('No puede retirar menos CANTIDADES NEGATIVAS')
    }
    
    else if(total_ret_anterior == total_retirada){
        estado = false //sin cambios
        alert('No se detectaron cambios.')
        console.log("NO RETIRO NADA, DETECTADO , retiro anterior = retiro actual")
    }
    else if( total_retirada > 0 && total_retirada < total_comprada){
        estado_retiro = 'INCOMPLETO'
        console.log("Retirado incompleto detectado")
    }
    else if(total_retirada == total_comprada){
        estado_retiro = 'COMPLETO'
        console.log('Retirado completamente detectado')
    }

    if(estado){
        
        new_dato = []
        new_dato.push(estado_retiro)
        new_dato.push(datos)
        new_dato.push(interno)
        //historial
        new_dato.push(l_descripciones)
        new_dato.push(l_ret_anterior)
        new_dato.push(l_retirado)
        console.log(new_dato)
        
        $.ajax({
            url: "/actualizar/nota_venta/item",
            type: "POST",
            data: JSON.stringify(new_dato),
            contentType: "application/json; charset=utf-8",
            success: function(resp){
                if(resp.data){
                    console.log(resp.message)
                    $('#modal_info').modal('hide')// SE OCULTA EL MODAL
                    $('#mensaje').empty()
                    tipo_alert = 'success'
                    $('#mensaje').append('<div class="alert alert-'+tipo_alert+'"><button type="button" class="close" data-dismiss="alert">&times;</button>'+tipo_doc +' '+folio+': '+resp.message+'</div>')

                    nueva_fecha = $("#fecha_docs").val()
                    cargar_body(nueva_fecha)

                }else{
                    $('#modal_info').modal('hide')// SE OCULTA EL MODAL
                    $('#mensaje').empty()
                    tipo_alert = 'warning'
                    $('#mensaje').append('<div class="alert alert-'+tipo_alert+'"><button type="button" class="close" data-dismiss="alert">&times;</button>'+tipo_doc +' '+folio+': '+resp.message+'</div>')
                }
            }
            
        })
    }

}

function guardar_cambios_2(interno){//ACTUALIZAR GUIA
    console.log("guardar 2")
    console.log(detalle)
    var tabla = document.getElementById('table_info1')
    estado = true // checkea si se actualiza el documento o no.
    estado_retiro = 'NO RETIRADO'
    total_retirada = 0
    total_comprada = 0
    total_ret_anterior = 0
    
    l_descripciones = []
    l_retirado = []
    l_ret_anterior = []
    
    for (var i = 1, row; row = tabla.rows[i]; i++) {
        item = []
        comprada = $('#item_max_'+ i.toString()).text()
        retirada = $('#item_ret_'+ i.toString()).val()
        if(retirada == ''){
            console.log('item vacio')
            estado = false
            retirada = 0
        }

        ret_anterior = detalle.retirado[i-1]
        if(ret_anterior == null){
            ret_anterior = 0
        }
        console.log("Fila: "+comprada + " - " + retirada + ' - anterior: ' + ret_anterior.toString() )
        
        comprada = parseFloat(comprada)
        retirada = parseFloat(retirada)
        if(retirada > comprada){
            estado = false
        }
        if(retirada < 0){
            estado = false
        }
        total_ret_anterior = total_ret_anterior + ret_anterior
        total_retirada = total_retirada + retirada
        total_comprada = total_comprada + comprada
    
        
    
        //historial
        l_descripciones.push(detalle.descripciones[i-1])
        l_ret_anterior.push( ret_anterior )
        l_retirado.push( parseFloat(retirada) )
        
    }
    console.log('TOTAL COMPRADA: ' + total_comprada.toString())
    console.log('TOTAL retirada actual: ' + total_retirada.toString())
    console.log('TOTAL ret ANTERIOR: ' + total_ret_anterior.toString())
    //console.log(datos)
    console.log(l_descripciones)
    console.log(l_ret_anterior)
    console.log(l_retirado)
    
    if(estado == false){
        alert('Un item supera la cantidad comprada o tiene un valor negativo')
        console.log('Un item supera la cantidad comprada o tiene un valor negativo')
    }
    else if(total_retirada > total_comprada){
        estado = false //no puede modificar el documento
        alert('No puede retirar mas de lo comprado')
        console.log('no puede retirar mas de lo comprado')
    }
    else if(total_retirada < 0 ){
        estado = false //no puede modificar el documento
        alert('No puede retirar cantidades negativas')
        console.log('No puede retirar menos CANTIDADES NEGATIVAS')
    }
    
    else if(total_ret_anterior == total_retirada){
        estado = false //sin cambios
        alert('No se detectaron cambios.')
        console.log("NO RETIRO NADA, DETECTADO , retiro anterior = retiro actual")
    }
    else if( total_retirada > 0 && total_retirada < total_comprada){
        estado_retiro = 'INCOMPLETO'
        console.log("Retirado incompleto detectado")
    }
    else if(total_retirada == total_comprada){
        estado_retiro = 'COMPLETO'
        console.log('Retirado completamente detectado')
    }
    if(estado){
        new_dato = []
        new_dato.push(estado_retiro)
        new_dato.push(l_retirado)
        new_dato.push(interno)
        //historial
        new_dato.push(l_descripciones)
        new_dato.push(l_ret_anterior)
        new_dato.push(l_retirado)
        console.log(new_dato)
        $.ajax({
            url: "/actualizar/guia/item",
            type: "POST",
            data: JSON.stringify(new_dato),
            contentType: "application/json; charset=utf-8",
            success: function(resp){
                if(resp.data){
                    console.log(resp.message)
                    $('#modal_info').modal('hide')// SE OCULTA EL MODAL
                    $('#mensaje').empty()
                    tipo_alert = 'success'
                    $('#mensaje').append('<div class="alert alert-'+tipo_alert+'"><button type="button" class="close" data-dismiss="alert">&times;</button>'+resp.message+'</div>')

                    nueva_fecha = $("#fecha_docs").val()
                    cargar_body(nueva_fecha)
                }else{
                    console.log(resp.message)
                    $('#modal_info').modal('hide')// SE OCULTA EL MODAL
                    $('#mensaje').empty()
                    tipo_alert = 'warning'
                    $('#mensaje').append('<div class="alert alert-'+tipo_alert+'"><button type="button" class="close" data-dismiss="alert">&times;</button>'+resp.message+'</div>')

                    //nueva_fecha = $("#fecha_docs").val()
                    //cargar_body(nueva_fecha)
                }
            }
            
        })
    }
    
}
function adjuntar(folio,tipo_doc,interno){
    console.log("adjuntando archivo")
    
    var fd = new FormData();
    var files = $('#archivo')[0].files;
    
    // Check file selected or not
    if(files.length > 0 ){
        fd.append('file',files[0]);

        $.ajax({
            url: '/subir/'+ folio.toString()+ '/'+ tipo_doc+ '/' + interno.toString(),
            type: 'post',
            data: fd,
            contentType: false,
            processData: false,
            success: function(resp){
                if(resp.category == "success"){
                    $('#modal_info').modal('hide')// SE OCULTA EL MODAL
                    $('#mensaje').empty()
                    tipo_alert = 'success'
                    $('#mensaje').append('<div class="alert alert-'+tipo_alert+'"><button type="button" class="close" data-dismiss="alert">&times;</button>'+resp.message+'</div>')
                    
                    nueva_fecha = $("#fecha_docs").val()
                    cargar_body(nueva_fecha)
                //$('#lista_adjuntos').append('<button type="button" class="list-group-item list-group-item-action">' + response.data+'<i class="fas fa-check-circle"></i></button>')
                }else{
                    $('#mensaje').empty()
                    tipo_alert = 'warning'
                    $('#mensaje').append('<div class="alert alert-'+tipo_alert+'"><button type="button" class="close" data-dismiss="alert">&times;</button>'+resp.message+'</div>')
            
                }
            },
        });
    }else{
        alert("Please select a file.");
    }
   
    
    
}
function buscar_historial(tipo,folio){
    let found3 = []
    console.log('buscando historial...')
    if(tipo== "BOLETA"){
        found3 = bol_historial.find(element => element[0] == folio )
    }
    else if(tipo=="FACTURA"){
         found3 = fact_historial.find(element => element[0] == folio )
        }
    else if(tipo =='GUIA'){
    
        if(respuesta[4] !=null){
            x_historial = JSON.parse(respuesta[4])
            found3 = [100 , x_historial]
        }else{
            found3 = null
        }
        
    }

    items_historial = ""
    nro_cambios = 0
    if(found3 != null){
        console.log(found3)
        lista = found3[1]
        console.log(lista)
        console.log(lista.lista_historial)
        for(let i = 0; i< lista.lista_historial.length ; i ++){
            historial = JSON.parse(lista.lista_historial[i])
            console.log(historial)
            console.log(historial.revisor)
            console.log(historial.fecha)
            
            h1 = '<li><button class="ver_cambio" onclick="ver_det_historial('+i.toString()+')">Fecha: '+ historial.fecha + ' | Revisor: '+ historial.revisor+'</button>'
            h2 = '<table style="display:None" id = "detalle_'+ i.toString() +'" class="tab_h"><thead><tr><th class="th_h">Descripcion</th><th class="th_h">Antes</th><th class="th_h">Despues</th></tr></thead><tbody>'
            h3 = ""
            for(let j = 0; j < historial.descripciones.length ; j ++){
                //BUG nro1: si el input esta vacio al guardar, se guardan valores null, que luego al leer causa error de tipo.
                let antes = historial.antes[j]
                let despues = historial.despues[j]

                if(antes == null) {
                    antes = 'None'
                }
                if(despues == null){
                    despues = 'None'
                }
                h3 = h3 + '<tr><td class="td_h">'+ historial.descripciones[j] +'</td><td class="td_h">'+ antes.toString() + '</td><td class="td_h">'+ despues.toString() +'</td></tr>'
               
            }
            
            h4 = '</tbody></table></li>'
            
            items_historial = items_historial + h1 + h2 + h3 + h4
            nro_cambios = nro_cambios + 1
        }

    }else{
        console.log('HISTORIAL NO ENCONTRADO')
    }
    return [items_historial,nro_cambios]
    /*
    if(found[1] != null){
        console.log('tiene historial')
        lista = found[1]
        for(let i = 0 ; i < lista.length ; i++){
            items_lista = items_lista + '<a href="/descargar/'+lista[i]+'">'+'<button type="button" class="list-group-item list-group-item-action">'+ lista[i] + '</button></a>'
            nro_adj = nro_adj + 1
        }
    }
    return [items_lista, nro_adj ]*/
}

function ver_adjuntos(){
    var x = document.getElementById("lista_adjuntos")
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function ver_vinculos(){
    var x = document.getElementById("lista_vinculos")
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
function ver_historial(){
    var x = document.getElementById("lista_historial")
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
function ver_det_historial(id){
    var x = document.getElementById("detalle_"+ id.toString())
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
function obtener_fecha(fecha){
    let date = new Date(fecha)

    let day = date.getDate()
    let month = date.getMonth() + 1
    let year = date.getFullYear()

    if(month < 10){
    return `${day}-0${month}-${year}`
    }else{
    return `${day}-${month}-${year}`
    }
}