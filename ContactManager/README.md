# Sistema de Gerenciamento de Contatos

Este projeto implementa um sistema de gerenciamento de contatos em Java, utilizando listas encadeadas como estrutura de dados principal. O sistema permite adicionar, buscar, remover e listar contatos através de uma interface de linha de comando.

## Sumário
1. [Visão Geral](#visão-geral)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Requisitos do Sistema](#requisitos-do-sistema)
4. [Instalação e Execução](#instalação-e-execução)
5. [Funcionalidades](#funcionalidades)
6. [Implementação](#implementação)
7. [Algoritmos Utilizados](#algoritmos-utilizados)
8. [Exemplos de Uso](#exemplos-de-uso)
9. [Considerações sobre Desempenho](#considerações-sobre-desempenho)
10. [Possíveis Melhorias](#possíveis-melhorias)
11. [Autores](#autores)

## Visão Geral

O Sistema de Gerenciamento de Contatos foi desenvolvido como um projeto acadêmico para a disciplina de Análise e Desenvolvimento de Sistemas. O objetivo principal é implementar um sistema que permita gerenciar uma lista de contatos utilizando conceitos fundamentais de estruturas de dados, especificamente listas encadeadas.

## Estrutura do Projeto

O projeto é composto por quatro classes principais:

1. **Contact**: Representa um contato individual com nome, número de telefone e e-mail.
2. **Node**: Representa um nó na lista encadeada, contendo um objeto Contact e uma referência para o próximo nó.
3. **ContactList**: Implementa a lista encadeada e os métodos para manipulação dos contatos.
4. **ContactManager**: Contém o método main e gerencia a interação do usuário com o sistema através de um menu.

## Requisitos do Sistema

- Java Development Kit (JDK) 8 ou superior
- Ambiente de execução Java (JRE)
- Terminal ou prompt de comando

## Instalação e Execução

### Passo 1: Obter os arquivos do projeto
Clone o repositório ou baixe os arquivos para seu computador.

### Passo 2: Compilar o projeto
Abra um terminal ou prompt de comando, navegue até o diretório onde estão os arquivos e execute:

```bash
javac Contact.java Node.java ContactList.java ContactManager.java
```

### Passo 3: Executar o programa
Após a compilação, execute o programa com o comando:

```bash
java ContactManager
```

## Funcionalidades

O sistema oferece as seguintes funcionalidades:

1. **Adicionar Contato**: Permite adicionar um novo contato com nome, telefone e e-mail.
2. **Buscar Contato**: Permite buscar um contato pelo nome ou número de telefone.
3. **Remover Contato**: Permite remover um contato da lista pelo nome ou número de telefone.
4. **Listar Contatos**: Exibe todos os contatos armazenados na lista.
5. **Sair**: Encerra o programa.

## Implementação

### Classe Contact
```java
public class Contact {
    private String name;
    private String phoneNumber;
    private String email;
    
    // Constructor, getters, toString()
    // ...
}
```

A classe `Contact` encapsula os dados de um contato e fornece métodos para acessar esses dados. O método `toString()` é implementado para exibir as informações do contato de forma formatada.

### Classe Node
```java
public class Node {
    private Contact contact;
    private Node next;
    
    // Constructor, getters, setters
    // ...
}
```

A classe `Node` representa um nó na lista encadeada. Cada nó contém um objeto `Contact` e uma referência para o próximo nó na lista.

### Classe ContactList
```java
public class ContactList {
    private Node head;
    
    // Constructor, addContact(), searchContact(), removeContact(), listContacts()
    // ...
}
```

A classe `ContactList` implementa a estrutura de lista encadeada e os métodos para manipulação dos contatos. O atributo `head` referencia o primeiro nó da lista.

### Classe ContactManager
```java
public class ContactManager {
    public static void main(String[] args) {
        // Menu de interação com o usuário
        // ...
    }
}
```

A classe `ContactManager` contém o método `main` e implementa a interface de linha de comando para interação com o usuário.

## Algoritmos Utilizados

### Algoritmo de Busca Linear
Para a funcionalidade de busca de contatos, foi implementado um algoritmo de busca linear. Este algoritmo percorre a lista do início até o fim, verificando cada nó até encontrar o contato desejado ou chegar ao final da lista.

A complexidade de tempo deste algoritmo é O(n), onde n é o número de contatos na lista.

```java
public Contact searchContact(String nameOrPhone) {
    if (head == null) {
        return null;
    }
    
    Node current = head;
    while (current != null) {
        Contact contact = current.getContact();
        if (contact.getName().equalsIgnoreCase(nameOrPhone) || 
            contact.getPhoneNumber().equals(nameOrPhone)) {
            return contact;
        }
        current = current.getNext();
    }
    
    return null; // Contact not found
}
```

### Algoritmo de Inserção
Para adicionar um contato, o algoritmo percorre a lista até o último nó e adiciona o novo nó no final. Se a lista estiver vazia, o novo nó se torna o `head`.

A complexidade de tempo deste algoritmo é O(n), onde n é o número de contatos na lista.

### Algoritmo de Remoção
Para remover um contato, o algoritmo busca o nó que contém o contato desejado e ajusta as referências para remover esse nó da lista. É necessário um tratamento especial quando o nó a ser removido é o `head`.

A complexidade de tempo deste algoritmo também é O(n).

## Exemplos de Uso

### Adicionar um Contato:
1. Selecione a opção 1 no menu.
2. Digite o nome do contato.
3. Digite o número de telefone.
4. Digite o e-mail.

### Buscar um Contato:
1. Selecione a opção 2 no menu.
2. Digite o nome ou número de telefone do contato que deseja buscar.
3. O sistema exibirá as informações do contato, se encontrado.

### Remover um Contato:
1. Selecione a opção 3 no menu.
2. Digite o nome ou número de telefone do contato que deseja remover.
3. O sistema removerá o contato da lista e exibirá uma mensagem de confirmação.

### Listar Todos os Contatos:
1. Selecione a opção 4 no menu.
2. O sistema exibirá todos os contatos armazenados na lista.

## Considerações sobre Desempenho

A implementação atual utiliza uma lista encadeada simples, que é eficiente para inserções no final da lista, mas tem complexidade O(n) para operações de busca e remoção. Para grandes volumes de dados, estruturas como tabelas hash ou árvores de busca podem oferecer melhor desempenho.

## Possíveis Melhorias

1. **Implementação de persistência de dados**: Salvar os contatos em um arquivo ou banco de dados para preservá-los entre execuções do programa.
2. **Interface gráfica**: Desenvolver uma interface gráfica para melhorar a experiência do usuário.
3. **Estruturas de dados mais eficientes**: Utilizar estruturas como tabelas hash para melhorar o desempenho de busca.
4. **Validação de dados**: Implementar validação para os dados de entrada, como formato de e-mail e número de telefone.
5. **Funcionalidades adicionais**: Adicionar funcionalidades como edição de contatos, categorização, etc.

## Autor

João Rafael Ferrão - jrferrao@gmail.com

---

Desenvolvido como projeto para a disciplina de Programação Orientada a Objetos II, do curso de Analise e Desenvolvimento de Sistemas no Centro Universitário de Brasília (CEUB).