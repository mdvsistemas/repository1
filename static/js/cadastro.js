const clienteCadastro = document.querySelector("#clienteCadastro");

clienteCadastro.addEventListener('submit', (event) =>{
    event.preventDefault();
    let senha = document.querySelector("#senhaCliente");
    let repetirSenha = document.querySelector("#repetirSenha");
    let msgErro = document.querySelector("#msgErro");

    if (senha.value !== repetirSenha.value) {
        msgErro.style.display = 'block';
        repetirSenha.style.background = 'red';
        senha.style.background = 'red';
        return false;
    }else{
        msgErro.style.display = 'none';
        repetirSenha.style.background = 'white';
        senha.style.background = 'white';
        clienteCadastro.submit();
        return true;
    }
})