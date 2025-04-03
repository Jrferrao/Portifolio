public class Contact {
    private String name;
    private String phoneNumber;
    private String email;
    
    // Constructor
    public Contact(String name, String phoneNumber, String email) {
        this.name = name;
        this.phoneNumber = phoneNumber;
        this.email = email;
    }
    
    // Getters
    public String getName() {
        return name;
    }
    
    public String getPhoneNumber() {
        return phoneNumber;
    }
    
    public String getEmail() {
        return email;
    }
    
    // toString method for displaying contact information
    @Override
    public String toString() {
        return "Nome: " + name + 
               "\nTelefone: " + phoneNumber + 
               "\nEmail: " + email;
    }
}