import java.util.*

public class Main {
    public static void main(String[] args) {
        int n = 10;
        long a = 0, b = 1;

        System.out.println("First " + n + " Fibonacci numbers:");
        for (int i = 0; i < n; i++) {
            System.out.print(a + " ");
            long next = a + b;
            a = b;
            b = next;
        }
    }
}