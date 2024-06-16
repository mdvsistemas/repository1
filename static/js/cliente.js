

const btnapagar_conta = document.querySelector(".apagar_conta");
const modal_apagarConta = document.querySelector("#modal_apagarConta");
const cancelarApagarConta = document.querySelector("#cancelarApagarConta");
const btnEscolha_formulario_senha = document.querySelector("#escolha_formulario_senha");
const produtos = document.querySelector("#produtos");
const formulario_senha = document.querySelector("#formulario_senha");
const titulo = document.querySelector("#titulo");
const btnHistorico = document.querySelector("#btnHistorico");
const paginaInicial = document.querySelector("#paginaInicial");
const Meus_pedidos = document.querySelector("#Meus_pedidos");
const historico = document.querySelector("#historico");



escolha_formulario_senha.addEventListener("click", ()=>{
    produtos.style.display = 'none';
    formulario_senha.style.display = 'flex';
    historico.style.display = 'none';
    titulo.textContent = "Mudar Senha";

})



const formNovaSenha = document.querySelector('#formMudarSenha');
const novaSenha = document.querySelector('#novaSenha');
const repetirnovaSenha = document.querySelector('#repetirNovaSenha');
const mensagemerro = document.querySelector('#errosenha');
formNovaSenha.addEventListener('submit',(e) =>{
    if (novaSenha.value !== repetirnovaSenha.value){
        mensagemerro.textContent = 'Senhas não combinam!';
        e.preventDefault();
    }
})