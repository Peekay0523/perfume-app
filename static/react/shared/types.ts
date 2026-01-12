import z from "zod";

export const PerfumeSchema = z.object({
  id: z.number(),
  name: z.string(),
  brand: z.string(),
  description: z.string().nullable(),
  price: z.number(),
  image_url: z.string().nullable(),
  size_ml: z.number().nullable(),
  notes: z.string().nullable(),
  created_at: z.string(),
  updated_at: z.string(),
});

export type Perfume = z.infer<typeof PerfumeSchema>;

export const CartItemSchema = z.object({
  id: z.number(),
  quantity: z.number(),
  perfume_id: z.number(),
  name: z.string(),
  brand: z.string(),
  description: z.string().nullable(),
  price: z.number(),
  image_url: z.string().nullable(),
  size_ml: z.number().nullable(),
  notes: z.string().nullable(),
});

export type CartItem = z.infer<typeof CartItemSchema>;

export const OrderSchema = z.object({
  id: z.number(),
  user_id: z.string(),
  total: z.number(),
  status: z.string(),
  customer_name: z.string().nullable(),
  customer_email: z.string().nullable(),
  shipping_address: z.string().nullable(),
  created_at: z.string(),
  updated_at: z.string(),
});

export type Order = z.infer<typeof OrderSchema>;

export const OrderItemSchema = z.object({
  id: z.number(),
  order_id: z.number(),
  perfume_id: z.number(),
  quantity: z.number(),
  price: z.number(),
  name: z.string(),
  brand: z.string(),
  image_url: z.string().nullable(),
});

export type OrderItem = z.infer<typeof OrderItemSchema>;

export interface OrderWithItems extends Order {
  items: OrderItem[];
}
