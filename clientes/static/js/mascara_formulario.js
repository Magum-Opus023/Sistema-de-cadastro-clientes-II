document.addEventListener("DOMContentLoaded", function() {
    function aplicarMascara(input, mascara) {
        input.addEventListener("input", function() {
            let valor = input.value.replace(/\D/g, "");
            let padrao = mascara.replace(/\D/g, "");
            let resultado = "";
            let j = 0;

            for (let i = 0; i < mascara.length; i++) {
                if (mascara[i] === "_") {
                    if (valor[j]) {
                        resultado += valor[j++];
                    } else {
                        break;
                    }
                } else {
                    resultado += mascara[i];
                }
            }

            input.value = resultado;
        });
    }

    // CPF: 000.000.000-00
    const cpfInput = document.getElementById("id_cpf");
    if (cpfInput) aplicarMascara(cpfInput, "___.___.___-__");

    // Telefone (celular): (00) 00000-0000
    const telefoneInput = document.getElementById("id_telefone");
    if (telefoneInput) aplicarMascara(telefoneInput, "(__) _____-____");

    // CEP: 00000-000
    const cepInput = document.getElementById("id_cep");
    if (cepInput) aplicarMascara(cepInput, "_____-___");

    // Aniversário: 00/00
    const aniversarioInput = document.getElementById("id_aniversario");
    if (aniversarioInput) aplicarMascara(aniversarioInput, "__/__");
});