
document.addEventListener("DOMContentLoaded", function() {
    
    const sidebar_collapse_menus = document.querySelectorAll('.open-menu');

    sidebar_collapse_menus.forEach(element => element.addEventListener('click', () => {

        sidebar_collapse_menus.forEach(menus => {

            if (element.getAttribute('href') !== menus.getAttribute('href')) {

                const submenu = document.getElementById(menus.getAttribute('href').replace('#', ''));

                var bsCollapse = new bootstrap.Collapse(submenu, {
                    toggle: false
                });

                bsCollapse.hide();

                const arrow_icon = menus.querySelector('.icon-rotates');

                if (!arrow_icon.style.transform == '' || !arrow_icon.style.transform == 'none') {
                    arrow_icon.style.transform = '';
                }

            }

        });

        const arrow_icon = element.querySelector('.icon-rotates');

        if (arrow_icon.style.transform == '' || arrow_icon.style.transform == 'none') {
            arrow_icon.style.transform = 'rotate(90deg)'
        } else {
            arrow_icon.style.transform = '';
        }
    }));

    function abrirModalConfirmacaoGeral(data, refresh = true) {

        const modal_confirmacao_geral = new bootstrap.Modal(document.getElementById('confirmacao-geral-modal'), {
            keyboard: false
        });

        var modal_title = document.getElementById('confirmacao-geral-modal').querySelector('.modal-title');
        var modal_body = document.getElementById('confirmacao-geral-modal').querySelector('.modal-body');

        modal_title.textContent = data.title;
        modal_body.innerHTML = data.body;

        modal_confirmacao_geral.show();

        document.getElementById('confirmacao-geral-modal').addEventListener('hidden.bs.modal', function(event) {

            if (refresh) {
                window.location.reload();
            }

        });

    }

    function closeModal(modalObject) {

        const get_modal = document.getElementById(modalObject);
        const modal = bootstrap.Modal.getInstance(get_modal);
        modal.hide();

    };

    function postForms(url, method, formData, refresh = true) {

        fetch(url, {
                method: method,
                body: formData
            })
            .then(response => response.json())
            .then(data => {

                abrirModalConfirmacaoGeral(data, refresh);

            });

    };

    function submitButtonSpinner(button_id) {

        const button = document.getElementById(button_id);

        button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Aguarde';
        button.setAttribute('disabled', 'disabled');

    }


    if (document.getElementById('main-listas-usuario')) {

        document.querySelectorAll('.editUsuario').forEach(element => element.addEventListener('click', function() {
            fetch('/dadosUsuario', {
                method: "POST",
                body: JSON.stringify({ 'txtEditUsuarioID': this.getAttribute('data-id') }),
                headers: {
                    'Content-Type': 'application/json; charset=UTF-8'
                }
            })
            .then(response => {
                console.log(response)

                return response.json();
            })
            .then(data => {
                var modal = new bootstrap.Modal(document.getElementById('editar-usuario-modal'), {
                    keyboard: false
                });
        
                document.getElementById('editar-usuario-modal').querySelector('#txtEditusuarioID').value = this.getAttribute('data-id');
                document.getElementById('editar-usuario-modal').querySelector('#txtEditarNome').value = data.nome;
                document.getElementById('editar-usuario-modal').querySelector('#txtEditarEmail').value = data.email;
                document.getElementById('editar-usuario-modal').querySelector('#txtEditarTelefone').value = data.telefone;
                document.getElementById('editar-usuario-modal').querySelector('#txtEditarProfissao').value = data.profissao;
                document.getElementById('editar-usuario-modal').querySelector('#txtEditarArea').value = data.area;
        
                modal.show();
            })
        }))

        document.getElementById('editar-usuario-form').addEventListener('submit', function(event) {
            closeModal('editar-usuario-modal')
            event.preventDefault();
            var form = new FormData(this);
            postForms(this.action, this.method, form);
        })

        document.querySelectorAll('.deleteUsuario').forEach(element => element.addEventListener('click', function() {
            var modal = new bootstrap.Modal(document.getElementById('deletar-usuario-modal'), {
                keyboard: false
            });

            document.getElementById('deletar-usuario-modal').querySelector('#txtDeleteusuarioID').value = this.getAttribute('data-id');

            modal.show()
        }))


        document.getElementById('deletar-usuario-form').addEventListener('submit', function(event) {
            closeModal('deletar-usuario-modal')
            event.preventDefault();
            var form = new FormData(this);
            postForms(this.action, this.method, form);
        })

        

        document.getElementById('cadastrar-usuario-form').addEventListener('submit', function(event) {
            submitButtonSpinner('btnCadastrarUsuario')
            event.preventDefault();
            var form = new FormData(this);
            postForms(this.action, this.method, form);
        })


        $('#tblUsuarios').DataTable({
            dom: "<'row'<'col-sm-12 col-md-4'B><'col-sm-12 col-md-4'l><'col-sm-12 col-md-4'f>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            buttons: [{
                extend: 'excelHtml5',
                exportOptions: {
                    columns: ':not(:last-child)'
                }
            }],
            columnDefs: [{
                targets: [-1],
                orderable: false,
            }],
            order: [
                [0, "desc"]
            ],
            language: {
                lengthMenu: "Mostrar _MENU_ registros por página",
                zeroRecords: "Nada encontrado - desculpa =/",
                info: "Total de _TOTAL_ registros",
                infoEmpty: "Nenhum registro encontrado",
                infoFiltered: "(Filtrado de _MAX_ registros)",
                search: '',
                searchPlaceholder: "Faça sua busca",
                paginate: {
                    first: "Primeira",
                    last: "Última",
                    next: "Próxima",
                    previous: "Anterior",
                },
                emptyTable: "Nada para mostrar aqui!",
            },
            lengthMenu: [
                [5, 10, 15, 20, 25, -1],
                [5, 10, 15, 20, 25, "Todos"]
            ],
            pageLength: 25,
            responsive: true
        });

        $('#txtCadastrarContato, #txtEditarTelefone').mask('(00) 0000-0000');
    }

    if (document.getElementById('main-listas-requisicoes-cadastrar')) {
        document.getElementById('cadastrar-requisicao-form').addEventListener('submit', function(event) {
            submitButtonSpinner('btnCadastrarRequisicao')
            event.preventDefault();
            var form = new FormData(this);
            postForms(this.action, this.method, form);
        })

        $('#txtCadastrarDataExpectativa').mask('00/00/0000');
    }

    if (document.getElementById('main-requisicoes-detalhes')) {
        if (document.getElementById('analisar-requisicao-modal')) {
            document.getElementById('analisar-requisicao-form').addEventListener('submit', function(event) {
                closeModal('analisar-requisicao-modal');
                event.preventDefault();
                var form = new FormData(this);
                postForms(this.action, this.method, form);
            })
        }

        if (document.getElementById('concluir-requisicao-modal')) {
            document.getElementById('concluir-requisicao-form').addEventListener('submit', function(event) {
                closeModal('concluir-requisicao-modal');
                event.preventDefault();
                var form = new FormData(this);
                postForms(this.action, this.method, form);
            })
        }

        if (document.getElementById('editar-requisicao-modal')) {
            document.getElementById('editar-requisicao-form').addEventListener('submit', function(event) {
                closeModal('editar-requisicao-modal');
                event.preventDefault();
                var form = new FormData(this);
                postForms(this.action, this.method, form);
            })

            $('#txtEditarDataExpectativa').mask('00/00/0000');
        }
        
    }

    if (document.getElementById('main-requisicoes-novas')) {
        $('#tblRequisicoesNovas').DataTable({
            dom: "<'row'<'col-sm-12 col-md-4'B><'col-sm-12 col-md-4'l><'col-sm-12 col-md-4'f>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            buttons: [{
                extend: 'excelHtml5',
                exportOptions: {
                    columns: ':not(:last-child)'
                }
            }],
            columnDefs: [{
                targets: [-1],
                orderable: false,
            }],
            order: [
                [2, "desc"]
            ],
            language: {
                lengthMenu: "Mostrar _MENU_ registros por página",
                zeroRecords: "Nada encontrado - desculpa =/",
                info: "Total de _TOTAL_ registros",
                infoEmpty: "Nenhum registro encontrado",
                infoFiltered: "(Filtrado de _MAX_ registros)",
                search: '',
                searchPlaceholder: "Faça sua busca",
                paginate: {
                    first: "Primeira",
                    last: "Última",
                    next: "Próxima",
                    previous: "Anterior",
                },
                emptyTable: "Nada para mostrar aqui!",
            },
            lengthMenu: [
                [5, 10, 15, 20, 25, -1],
                [5, 10, 15, 20, 25, "Todos"]
            ],
            pageLength: 25,
            responsive: true
        });
    }

    if (document.getElementById('main-requisicoes-em-andamento')) {
        $('#tblRequisicoesEmAndamento').DataTable({
            dom: "<'row'<'col-sm-12 col-md-4'B><'col-sm-12 col-md-4'l><'col-sm-12 col-md-4'f>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            buttons: [{
                extend: 'excelHtml5',
                exportOptions: {
                    columns: ':not(:last-child)'
                }
            }],
            columnDefs: [{
                targets: [-1],
                orderable: false,
            }],
            order: [
                [3, "desc"]
            ],
            language: {
                lengthMenu: "Mostrar _MENU_ registros por página",
                zeroRecords: "Nada encontrado - desculpa =/",
                info: "Total de _TOTAL_ registros",
                infoEmpty: "Nenhum registro encontrado",
                infoFiltered: "(Filtrado de _MAX_ registros)",
                search: '',
                searchPlaceholder: "Faça sua busca",
                paginate: {
                    first: "Primeira",
                    last: "Última",
                    next: "Próxima",
                    previous: "Anterior",
                },
                emptyTable: "Nada para mostrar aqui!",
            },
            lengthMenu: [
                [5, 10, 15, 20, 25, -1],
                [5, 10, 15, 20, 25, "Todos"]
            ],
            pageLength: 25,
            responsive: true
        });
    }

    if (document.getElementById('main-requisicoes-concluidas')) {
        $('#tblRequisicoesConcluidas').DataTable({
            dom: "<'row'<'col-sm-12 col-md-4'B><'col-sm-12 col-md-4'l><'col-sm-12 col-md-4'f>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
            buttons: [{
                extend: 'excelHtml5',
                exportOptions: {
                    columns: ':not(:last-child)'
                }
            }],
            columnDefs: [{
                targets: [-1],
                orderable: false,
            }],
            order: [
                [3, "desc"]
            ],
            language: {
                lengthMenu: "Mostrar _MENU_ registros por página",
                zeroRecords: "Nada encontrado - desculpa =/",
                info: "Total de _TOTAL_ registros",
                infoEmpty: "Nenhum registro encontrado",
                infoFiltered: "(Filtrado de _MAX_ registros)",
                search: '',
                searchPlaceholder: "Faça sua busca",
                paginate: {
                    first: "Primeira",
                    last: "Última",
                    next: "Próxima",
                    previous: "Anterior",
                },
                emptyTable: "Nada para mostrar aqui!",
            },
            lengthMenu: [
                [5, 10, 15, 20, 25, -1],
                [5, 10, 15, 20, 25, "Todos"]
            ],
            pageLength: 25,
            responsive: true
        });
    }

});
