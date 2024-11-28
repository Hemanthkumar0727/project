import random
import math
from collections import defaultdict

# Set the number of customers to generate
num_customers = 30  # Change this value to generate more or fewer customers

# Generate synthetic customer data
customers = []
for i in range(1, num_customers + 1):  # Create customers based on num_customers
    customers.append({
        "Customer_ID": i,
        "Age": random.randint(18, 70),
        "Annual_Income": random.randint(20000, 120000),
        "Spending_Score": random.randint(1, 100)
    })

# Step 1: Display the customer data
print("Customer Data:")
for customer in customers:
    print(customer)

# Step 2: Normalize data manually
def normalize(data, key):
    values = [customer[key] for customer in data]
    min_val = min(values)
    max_val = max(values)
    for customer in data:
        customer[f"{key}_normalized"] = (customer[key] - min_val) / (max_val - min_val)

normalize(customers, "Age")
normalize(customers, "Annual_Income")
normalize(customers, "Spending_Score")

# Step 3: Manual K-Means Clustering
def euclidean_distance(c1, c2):
    return math.sqrt(
        (c1['Age_normalized'] - c2['Age_normalized'])**2 +
        (c1['Annual_Income_normalized'] - c2['Annual_Income_normalized'])**2 +
        (c1['Spending_Score_normalized'] - c2['Spending_Score_normalized'])**2
    )

def kmeans(data, k=3, max_iterations=10):
    # Randomly initialize centroids
    centroids = random.sample(data, k)
    clusters = defaultdict(list)

    for _ in range(max_iterations):
        # Assign customers to the nearest centroid
        clusters.clear()
        for customer in data:
            distances = [euclidean_distance(customer, centroid) for centroid in centroids]
            nearest = distances.index(min(distances))
            clusters[nearest].append(customer)

        # Recalculate centroids
        new_centroids = []
        for cluster in clusters.values():
            if cluster:  # Avoid empty clusters
                avg_age = sum(c['Age_normalized'] for c in cluster) / len(cluster)
                avg_income = sum(c['Annual_Income_normalized'] for c in cluster) / len(cluster)
                avg_score = sum(c['Spending_Score_normalized'] for c in cluster) / len(cluster)
                new_centroids.append({'Age_normalized': avg_age, 'Annual_Income_normalized': avg_income, 'Spending_Score_normalized': avg_score})
            else:
                new_centroids.append(random.choice(data))  # Reinitialize empty clusters
        centroids = new_centroids

    return clusters

clusters = kmeans(customers)

# Step 4: Display clusters
print("\nCustomer Clusters:")
for cluster_id, cluster_customers in clusters.items():
    print(f"\nCluster {cluster_id + 1}:")
    for customer in cluster_customers:
        print(f"Customer ID: {customer['Customer_ID']} - Age: {customer['Age']}, Income: {customer['Annual_Income']}, Score: {customer['Spending_Score']}")

# Step 5: Simple Recommendation Logic
def recommend_products(customer, all_customers, num_recommendations=3):
    distances = [(other, euclidean_distance(customer, other)) for other in all_customers if other != customer]
    distances.sort(key=lambda x: x[1])
    recommended_customers = [d[0] for d in distances[:num_recommendations]]
    return [f"Customer ID {rc['Customer_ID']}" for rc in recommended_customers]

# Commenting out the recommendation output
# print("\nRecommendations:")
# for customer in customers[:3]:  # Recommend for first 3 customers
#     recommendations = recommend_products(customer, customers)
#     print(f"Customer ID {customer['Customer_ID']} should connect with: {', '.join(recommendations)}")
