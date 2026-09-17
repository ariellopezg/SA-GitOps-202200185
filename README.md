## Descripción

Este repositorio indica qué aplicaciones y versiones deben estar ejecutándose
en Kubernetes. Argo CD lo revisa constantemente y mantiene el clúster igual a
lo definido aquí.

El código fuente, las pruebas y la construcción de imágenes están en el
repositorio principal. Este repositorio contiene únicamente la configuración
que Argo CD necesita para desplegar esas imágenes.

## Carpetas

- `applications/`: contiene un chart de Helm por cada microservicio y por cada
  componente de soporte, como PostgreSQL, RabbitMQ y los CronJobs. Cada chart
  incluye valores diferentes para desarrollo y producción.
- `environments/development/`: crea las aplicaciones de Argo CD que despliegan
  los charts en el namespace `development`.
- `environments/production/`: crea las aplicaciones de Argo CD que despliegan
  los charts en el namespace `production`.

## Flujo de un cambio

1. GitHub Actions construye y publica una nueva versión de una imagen.
2. El pipeline abre un pull request en este repositorio para cambiar su
   `image.tag`.
3. Al aceptar el pull request, la nueva versión queda registrada en `main`.
4. Argo CD detecta el cambio y sincroniza el ambiente correspondiente.
5. Argo Rollouts entrega tráfico gradualmente a la nueva versión mediante la
   estrategia canary.

GitHub Actions no despliega directamente en Kubernetes. Argo CD es el único
encargado de aplicar al clúster los cambios aceptados en este repositorio.
