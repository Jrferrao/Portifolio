import java.util.Scanner;

public class ContactManager {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        ContactList contactList = new ContactList();
        
        boolean running = true;
        
        System.out.println("Sistema de Gerenciamento de Contatos");
        
        while (running) {
            System.out.println("\n===== MENU =====");
            System.out.println("1. Adicionar Contato");
            System.out.println("2. Buscar Contato");
            System.out.println("3. Remover Contato");
            System.out.println("4. Listar Contatos");
            System.out.println("5. Sair");
            System.out.print("Escolha uma opção: ");
            
            int choice;
            try {
                choice = Integer.parseInt(scanner.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("Entrada inválida. Por favor, digite um número.");
                continue;
            }
            
            switch (choice) {
                case 1:
                    // Add a contact
                    System.out.println("\n--- Adicionar Contato ---");
                    System.out.print("Nome: ");
                    String name = scanner.nextLine();
                    
                    System.out.print("Telefone: ");
                    String phoneNumber = scanner.nextLine();
                    
                    System.out.print("Email: ");
                    String email = scanner.nextLine();
                    
                    Contact newContact = new Contact(name, phoneNumber, email);
                    contactList.addContact(newContact);
                    System.out.println("Contato adicionado com sucesso!");
                    break;
                    
                case 2:
                    // Search for a contact
                    System.out.println("\n--- Buscar Contato ---");
                    System.out.print("Digite o nome ou telefone: ");
                    String searchTerm = scanner.nextLine();
                    
                    Contact foundContact = contactList.searchContact(searchTerm);
                    if (foundContact != null) {
                        System.out.println("\nContato encontrado:");
                        System.out.println(foundContact.toString());
                    } else {
                        System.out.println("Contato não encontrado.");
                    }
                    break;
                    
                case 3:
                    // Remove a contact
                    System.out.println("\n--- Remover Contato ---");
                    System.out.print("Digite o nome ou telefone: ");
                    String removeTerm = scanner.nextLine();
                    
                    boolean removed = contactList.removeContact(removeTerm);
                    if (removed) {
                        System.out.println("Contato removido com sucesso!");
                    } else {
                        System.out.println("Contato não encontrado.");
                    }
                    break;
                    
                case 4:
                    // List all contacts
                    System.out.println("\n--- Lista de Contatos ---");
                    contactList.listContacts();
                    break;
                    
                case 5:
                    // Exit the program
                    running = false;
                    System.out.println("Encerrando o programa. Obrigado por usar o Sistema de Gerenciamento de Contatos!");
                    break;
                    
                default:
                    System.out.println("Opção inválida. Por favor, tente novamente.");
            }
        }
        
        scanner.close();
    }
}