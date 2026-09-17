{{- define "likes-service.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "likes-service.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- include "likes-service.name" . }}
{{- end }}
{{- end }}

{{- define "likes-service.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" }}
{{ include "likes-service.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "likes-service.selectorLabels" -}}
app.kubernetes.io/name: {{ include "likes-service.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

