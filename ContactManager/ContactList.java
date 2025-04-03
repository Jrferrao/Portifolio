public class ContactList {
    private Node head;
    
    // Constructor
    public ContactList() {
        this.head = null;
    }
    
    // Add a contact to the end of the list
    public void addContact(Contact contact) {
        Node newNode = new Node(contact);
        
        // If the list is empty, set the new node as the head
        if (head == null) {
            head = newNode;
            return;
        }
        
        // Otherwise, find the last node and append the new node
        Node current = head;
        while (current.getNext() != null) {
            current = current.getNext();
        }
        
        current.setNext(newNode);
    }
    
    // Search for a contact by name or phone number
    public Contact searchContact(String nameOrPhone) {
        if (head == null) {
            return null;
        }
        
        Node current = head;
        while (current != null) {
            Contact contact = current.getContact();
            // Check if the name or phone number matches
            if (contact.getName().equalsIgnoreCase(nameOrPhone) || 
                contact.getPhoneNumber().equals(nameOrPhone)) {
                return contact;
            }
            current = current.getNext();
        }
        
        return null; // Contact not found
    }
    
    // Remove a contact by name or phone number
    public boolean removeContact(String nameOrPhone) {
        if (head == null) {
            return false;
        }
        
        // If the head node contains the contact to be removed
        if (head.getContact().getName().equalsIgnoreCase(nameOrPhone) || 
            head.getContact().getPhoneNumber().equals(nameOrPhone)) {
            head = head.getNext();
            return true;
        }
        
        // Search for the contact in the rest of the list
        Node current = head;
        while (current.getNext() != null) {
            Contact nextContact = current.getNext().getContact();
            if (nextContact.getName().equalsIgnoreCase(nameOrPhone) || 
                nextContact.getPhoneNumber().equals(nameOrPhone)) {
                // Remove the node by updating the reference
                current.setNext(current.getNext().getNext());
                return true;
            }
            current = current.getNext();
        }
        
        return false; // Contact not found
    }
    
    // List all contacts
    public void listContacts() {
        if (head == null) {
            System.out.println("A lista de contatos está vazia.");
            return;
        }
        
        int count = 0;
        Node current = head;
        while (current != null) {
            count++;
            System.out.println("\nContato #" + count);
            System.out.println(current.getContact().toString());
            current = current.getNext();
        }
        
        System.out.println("\nTotal de contatos: " + count);
    }
}