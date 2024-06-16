function somaatualizarPreco() {
    var qtd = parseFloat(document.getElementById('hvalue').innerText);
    var preco = parseFloat(document.getElementById('preco').innerText);
    var unidade = (document.getElementById('unidade').innerText);
    if (unidade=='kg'){var multiplicador = parseFloat(document.getElementById('value').innerText)+0.15;}
    else {var multiplicador = parseFloat(document.getElementById('value').innerText)+1.00;}
    var novoPreco = (preco * multiplicador);
    var qtd = document.createElement

    document.getElementById('subtotal').innerText = novoPreco.toFixed(2);
    document.getElementById('value').innerText = multiplicador.toFixed(2);
    document.getElementById('hvalue').value = multiplicador.toFixed(2);
    
}

function subatualizarPreco() {
    var preco = parseFloat(document.getElementById('preco').innerText);
    var unidade = (document.getElementById('unidade').innerText);
    if (unidade=='kg'){var multiplicador = parseFloat(document.getElementById('value').innerText)-0.15;}
    else {var multiplicador = parseFloat(document.getElementById('value').innerText)-1.00;}
    if (multiplicador < 0) {multiplicador = 0}
    var novoPreco = preco * multiplicador;

    document.getElementById('subtotal').innerText = novoPreco.toFixed(2);
    document.getElementById('value').value = multiplicador.toFixed(2);
    
}

function resettotal() {
    var preco = parseFloat(document.getElementById('preco').innerText);
    var multiplicador = 0.00;
    var novoPreco = preco * multiplicador;

    document.getElementById('subtotal').innerText = novoPreco.toFixed(2);
    document.getElementById('value').innerText = multiplicador.toFixed(2);
}