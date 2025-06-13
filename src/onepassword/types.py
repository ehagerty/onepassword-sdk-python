"""
Generated by typeshare 1.13.2
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, PlainSerializer
from typing import Annotated, Dict, Generic, List, Literal, Optional, TypeVar, Union

E = TypeVar("E")
T = TypeVar("T")


def serialize_binary_data(value: bytes) -> list[int]:
    return list(value)


def deserialize_binary_data(value):
    if isinstance(value, list):
        if all(isinstance(x, int) and 0 <= x <= 255 for x in value):
            return bytes(value)
        raise ValueError("All elements must be integers in the range 0-255 (u8).")
    elif isinstance(value, bytes):
        return value
    raise TypeError("Content must be a list of integers (0-255) or bytes.")


def serialize_datetime_data(utc_time: datetime) -> str:
    return utc_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def parse_rfc3339(date_str: str) -> datetime:
    date_formats = ["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ"]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    raise ValueError(f"Invalid RFC 3339 date format: {date_str}")


ErrorMessage = str


class AddressFieldDetails(BaseModel):
    """
    Additional attributes for OTP fields.
    """

    street: str
    """
    The street address
    """
    city: str
    """
    The city
    """
    country: str
    """
    The country
    """
    zip: str
    """
    The ZIP code
    """
    state: str
    """
    The state
    """


class DocumentCreateParams(BaseModel):
    name: str
    """
    The name of the file
    """
    content: Annotated[
        bytes,
        BeforeValidator(deserialize_binary_data),
        PlainSerializer(serialize_binary_data),
    ]
    """
    The content of the file
    """


class FileAttributes(BaseModel):
    name: str
    """
    The name of the file
    """
    id: str
    """
    The ID of the file retrieved from the server
    """
    size: int
    """
    The size of the file in bytes
    """


class FileCreateParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    """
    The name of the file
    """
    content: Annotated[
        bytes,
        BeforeValidator(deserialize_binary_data),
        PlainSerializer(serialize_binary_data),
    ]
    """
    The content of the file
    """
    section_id: str = Field(alias="sectionId")
    """
    The section id where the file should be stored
    """
    field_id: str = Field(alias="fieldId")
    """
    The field id where the file should be stored
    """


class GeneratePasswordResponse(BaseModel):
    """
    For future use, if we want to return more information about the generated password.
    Currently, it only returns the password itself.
    """

    password: str
    """
    The generated password.
    """


class ItemCategory(str, Enum):
    LOGIN = "Login"
    SECURENOTE = "SecureNote"
    CREDITCARD = "CreditCard"
    CRYPTOWALLET = "CryptoWallet"
    IDENTITY = "Identity"
    PASSWORD = "Password"
    DOCUMENT = "Document"
    APICREDENTIALS = "ApiCredentials"
    BANKACCOUNT = "BankAccount"
    DATABASE = "Database"
    DRIVERLICENSE = "DriverLicense"
    EMAIL = "Email"
    MEDICALRECORD = "MedicalRecord"
    MEMBERSHIP = "Membership"
    OUTDOORLICENSE = "OutdoorLicense"
    PASSPORT = "Passport"
    REWARDS = "Rewards"
    ROUTER = "Router"
    SERVER = "Server"
    SSHKEY = "SshKey"
    SOCIALSECURITYNUMBER = "SocialSecurityNumber"
    SOFTWARELICENSE = "SoftwareLicense"
    PERSON = "Person"
    UNSUPPORTED = "Unsupported"


class ItemFieldType(str, Enum):
    TEXT = "Text"
    CONCEALED = "Concealed"
    CREDITCARDTYPE = "CreditCardType"
    CREDITCARDNUMBER = "CreditCardNumber"
    PHONE = "Phone"
    URL = "Url"
    TOTP = "Totp"
    EMAIL = "Email"
    REFERENCE = "Reference"
    SSHKEY = "SshKey"
    MENU = "Menu"
    MONTHYEAR = "MonthYear"
    ADDRESS = "Address"
    DATE = "Date"
    UNSUPPORTED = "Unsupported"


class ItemFieldDetailsTypes(str, Enum):
    OTP = "Otp"
    SSH_KEY = "SshKey"
    ADDRESS = "Address"


class ItemFieldDetailsOtp(BaseModel):
    """
    The computed OTP code and other details
    """

    type: Literal[ItemFieldDetailsTypes.OTP] = ItemFieldDetailsTypes.OTP
    content: OtpFieldDetails


class ItemFieldDetailsSshKey(BaseModel):
    """
    Computed SSH Key attributes
    """

    type: Literal[ItemFieldDetailsTypes.SSH_KEY] = ItemFieldDetailsTypes.SSH_KEY
    content: Optional[SshKeyAttributes]


class ItemFieldDetailsAddress(BaseModel):
    """
    Address components
    """

    type: Literal[ItemFieldDetailsTypes.ADDRESS] = ItemFieldDetailsTypes.ADDRESS
    content: Optional[AddressFieldDetails]


# Field type-specific attributes.
ItemFieldDetails = Union[
    ItemFieldDetailsOtp, ItemFieldDetailsSshKey, ItemFieldDetailsAddress
]


class ItemField(BaseModel):
    """
    Represents a field within an item.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    """
    The field's ID
    """
    title: str
    """
    The field's title
    """
    section_id: Optional[str] = Field(alias="sectionId", default=None)
    """
    The ID of the section containing the field. Built-in fields such as usernames and passwords don't require a section.
    """
    field_type: ItemFieldType = Field(alias="fieldType")
    """
    The field's type
    """
    value: str
    """
    The string representation of the field's value
    """
    details: Optional[ItemFieldDetails] = Field(default=None)
    """
    Field type-specific attributes.
    """


class ItemSection(BaseModel):
    """
    A section groups together multiple fields in an item.
    """

    id: str
    """
    The section's unique ID
    """
    title: str
    """
    The section's title
    """


class AutofillBehavior(str, Enum):
    """
    Controls the auto-fill behavior of a website.


    For more information, visit https://support.1password.com/autofill-behavior/
    """

    ANYWHEREONWEBSITE = "AnywhereOnWebsite"
    """
    Auto-fill any page that’s part of the website, including subdomains
    """
    EXACTDOMAIN = "ExactDomain"
    """
    Auto-fill only if the domain (hostname and port) is an exact match.
    """
    NEVER = "Never"
    """
    Never auto-fill on this website
    """


class Website(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    url: str
    """
    The website URL
    """
    label: str
    """
    The label of the website, e.g. 'website', 'sign-in address'
    """
    autofill_behavior: AutofillBehavior = Field(alias="autofillBehavior")
    """
    The auto-fill behavior of the website
    
    For more information, visit https://support.1password.com/autofill-behavior/
    """


class ItemFile(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    attributes: FileAttributes
    """
    the attributes of the file
    """
    section_id: str = Field(alias="sectionId")
    """
    the section id where the file should be stored
    """
    field_id: str = Field(alias="fieldId")
    """
    the field id where the file should be stored
    """


class Item(BaseModel):
    """
    Represents an active 1Password item.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    """
    The item's ID
    """
    title: str
    """
    The item's title
    """
    category: ItemCategory
    """
    The item's category
    """
    vault_id: str = Field(alias="vaultId")
    """
    The ID of the vault where the item is saved
    """
    fields: List[ItemField]
    """
    The item's fields
    """
    sections: List[ItemSection]
    """
    The item's sections
    """
    notes: str
    """
    The notes of the item
    """
    tags: List[str]
    """
    The item's tags
    """
    websites: List[Website]
    """
    The websites used for autofilling for items of the Login and Password categories.
    """
    version: int
    """
    The item's version
    """
    files: List[ItemFile]
    """
    The item's file fields
    """
    document: Optional[FileAttributes] = Field(default=None)
    """
    The document file for the Document item category
    """
    created_at: Annotated[
        datetime,
        BeforeValidator(parse_rfc3339),
        PlainSerializer(serialize_datetime_data),
    ] = Field(alias="createdAt")
    """
    The time the item was created at
    """
    updated_at: Annotated[
        datetime,
        BeforeValidator(parse_rfc3339),
        PlainSerializer(serialize_datetime_data),
    ] = Field(alias="updatedAt")
    """
    The time the item was updated at
    """


class ItemCreateParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    category: ItemCategory
    """
    The item's category
    """
    vault_id: str = Field(alias="vaultId")
    """
    The ID of the vault where the item is saved
    """
    title: str
    """
    The item's title
    """
    fields: Optional[List[ItemField]] = Field(default=None)
    """
    The item's fields
    """
    sections: Optional[List[ItemSection]] = Field(default=None)
    """
    The item's sections
    """
    notes: Optional[str] = Field(default=None)
    """
    The item's notes
    """
    tags: Optional[List[str]] = Field(default=None)
    """
    The item's tags
    """
    websites: Optional[List[Website]] = Field(default=None)
    """
    The websites used for autofilling for items of the Login and Password categories.
    """
    files: Optional[List[FileCreateParams]] = Field(default=None)
    """
    The item's files stored as fields
    """
    document: Optional[DocumentCreateParams] = Field(default=None)
    """
    The document file for the Document item type. Empty when the item isn't of Document type.
    """


class ItemState(str, Enum):
    """
    Represents the state of an item in the SDK.
    """

    ACTIVE = "active"
    """
    The item is active
    """
    ARCHIVED = "archived"
    """
    The item is archived meaning it's hidden from regular view and stored in the archive.
    """


class ItemOverview(BaseModel):
    """
    Represents a decrypted 1Password item overview.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    """
    The item's ID
    """
    title: str
    """
    The item's title
    """
    category: ItemCategory
    """
    The item's category
    """
    vault_id: str = Field(alias="vaultId")
    """
    The ID of the vault where the item is saved
    """
    websites: List[Website]
    """
    The websites used for autofilling for items of the Login and Password categories.
    """
    tags: List[str]
    """
    The item tags
    """
    created_at: Annotated[
        datetime,
        BeforeValidator(parse_rfc3339),
        PlainSerializer(serialize_datetime_data),
    ] = Field(alias="createdAt")
    """
    The time the item was created at
    """
    updated_at: Annotated[
        datetime,
        BeforeValidator(parse_rfc3339),
        PlainSerializer(serialize_datetime_data),
    ] = Field(alias="updatedAt")
    """
    The time the item was updated at
    """
    state: ItemState
    """
    Indicates the state of the item
    """


class ItemShareDuration(str, Enum):
    """
    The valid duration options for sharing an item
    """

    ONEHOUR = "OneHour"
    """
    The share will expire in one hour
    """
    ONEDAY = "OneDay"
    """
    The share will expire in one day
    """
    SEVENDAYS = "SevenDays"
    """
    The share will expire in seven days
    """
    FOURTEENDAYS = "FourteenDays"
    """
    The share will expire in fourteen days
    """
    THIRTYDAYS = "ThirtyDays"
    """
    The share will expire in thirty days
    """


class AllowedType(str, Enum):
    """
    The allowed types of item sharing, enforced by account policy
    """

    AUTHENTICATED = "Authenticated"
    """
    Allows creating share links with specific recipients
    """
    PUBLIC = "Public"
    """
    Allows creating public share links
    """


class AllowedRecipientType(str, Enum):
    """
    The allowed recipient types of item sharing, enforced by account policy
    """

    EMAIL = "Email"
    """
    Recipients can be specified by email address
    """
    DOMAIN = "Domain"
    """
    Recipients can be specified by domain
    """


class ItemShareFiles(BaseModel):
    """
    The file sharing policy
    """

    model_config = ConfigDict(populate_by_name=True)

    allowed: bool
    """
    Whether files can be included in item shares
    """
    max_size: int = Field(alias="maxSize")
    """
    The maximum encrypted size (in bytes) an included file can be
    """
    allowed_types: Optional[List[AllowedType]] = Field(
        alias="allowedTypes", default=None
    )
    """
    The allowed types of item sharing - either "Authenticated" (share to specific users) or "Public" (share to anyone with a link)
    """
    allowed_recipient_types: Optional[List[AllowedRecipientType]] = Field(
        alias="allowedRecipientTypes", default=None
    )
    """
    The allowed recipient types of item sharing - either "Email" or "Domain"
    """
    max_expiry: Optional[ItemShareDuration] = Field(alias="maxExpiry", default=None)
    """
    The maximum duration that an item can be shared for
    """
    default_expiry: Optional[ItemShareDuration] = Field(
        alias="defaultExpiry", default=None
    )
    """
    The default duration that an item is shared for
    """
    max_views: Optional[int] = Field(alias="maxViews", default=None)
    """
    The maximum number of times an item can be viewed. A null value means unlimited views
    """


class ItemShareAccountPolicy(BaseModel):
    """
    The account policy for sharing items, set by your account owner/admin
    This policy is enforced server-side when sharing items
    """

    model_config = ConfigDict(populate_by_name=True)

    max_expiry: ItemShareDuration = Field(alias="maxExpiry")
    """
    The maximum duration that an item can be shared for
    """
    default_expiry: ItemShareDuration = Field(alias="defaultExpiry")
    """
    The default duration that an item is shared for
    """
    max_views: Optional[int] = Field(alias="maxViews", default=None)
    """
    The maximum number of times an item can be viewed. A null value means unlimited views
    """
    allowed_types: List[AllowedType] = Field(alias="allowedTypes")
    """
    The allowed types of item sharing - either "Authenticated" (share to specific users) or "Public" (share to anyone with a link)
    """
    allowed_recipient_types: List[AllowedRecipientType] = Field(
        alias="allowedRecipientTypes"
    )
    """
    The allowed recipient types of item sharing - either "Email" or "Domain"
    """
    files: ItemShareFiles
    """
    The file sharing policy
    """


class ValidRecipientEmailInner(BaseModel):
    """
    Generated type representing the anonymous struct variant `Email` of the `ValidRecipient` Rust enum
    """

    email: str


class ValidRecipientDomainInner(BaseModel):
    """
    Generated type representing the anonymous struct variant `Domain` of the `ValidRecipient` Rust enum
    """

    domain: str


class ValidRecipientTypes(str, Enum):
    EMAIL = "Email"
    DOMAIN = "Domain"


class ValidRecipientEmail(BaseModel):
    """
    This exact email address
    """

    type: Literal[ValidRecipientTypes.EMAIL] = ValidRecipientTypes.EMAIL
    parameters: ValidRecipientEmailInner


class ValidRecipientDomain(BaseModel):
    """
    Anyone with an email address from the specified domain
    """

    type: Literal[ValidRecipientTypes.DOMAIN] = ValidRecipientTypes.DOMAIN
    parameters: ValidRecipientDomainInner


# The validated recipient of an item share
ValidRecipient = Union[ValidRecipientEmail, ValidRecipientDomain]


class ItemShareParams(BaseModel):
    """
    The configuration options for sharing an item
    These must respect the account policy on item sharing
    """

    model_config = ConfigDict(populate_by_name=True)

    recipients: Optional[List[ValidRecipient]] = Field(default=None)
    """
    Emails or domains of the item share recipients. If not provided, everyone with the share link will have access
    """
    expire_after: Optional[ItemShareDuration] = Field(alias="expireAfter", default=None)
    """
    The duration of the share in seconds. If not provided, defaults to the account policy's default expiry
    """
    one_time_only: bool = Field(alias="oneTimeOnly")
    """
    Whether the item can only be viewed once per recipient
    """


class OtpFieldDetails(BaseModel):
    """
    Additional attributes for OTP fields.
    """

    model_config = ConfigDict(populate_by_name=True)

    code: Optional[str] = Field(default=None)
    """
    The OTP code, if successfully computed
    """
    error_message: Optional[str] = Field(alias="errorMessage", default=None)
    """
    The error message, if the OTP code could not be computed
    """


class Response(BaseModel, Generic[T, E]):
    content: Optional[T] = Field(default=None)
    error: Optional[E] = Field(default=None)


class ResolvedReference(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    secret: str
    item_id: str = Field(alias="itemId")
    vault_id: str = Field(alias="vaultId")


class ResolveReferenceErrorTypes(str, Enum):
    PARSING = "parsing"
    FIELD_NOT_FOUND = "fieldNotFound"
    VAULT_NOT_FOUND = "vaultNotFound"
    TOO_MANY_VAULTS = "tooManyVaults"
    ITEM_NOT_FOUND = "itemNotFound"
    TOO_MANY_ITEMS = "tooManyItems"
    TOO_MANY_MATCHING_FIELDS = "tooManyMatchingFields"
    NO_MATCHING_SECTIONS = "noMatchingSections"
    INCOMPATIBLE_TOTP_QUERY_PARAMETER_FIELD = "incompatibleTOTPQueryParameterField"
    UNABLE_TO_GENERATE_TOTP_CODE = "unableToGenerateTotpCode"
    S_SH_KEY_METADATA_NOT_FOUND = "sSHKeyMetadataNotFound"
    UNSUPPORTED_FILE_FORMAT = "unsupportedFileFormat"
    INCOMPATIBLE_SSH_KEY_QUERY_PARAMETER_FIELD = "incompatibleSshKeyQueryParameterField"
    UNABLE_TO_PARSE_PRIVATE_KEY = "unableToParsePrivateKey"
    UNABLE_TO_FORMAT_PRIVATE_KEY_TO_OPEN_SSH = "unableToFormatPrivateKeyToOpenSsh"
    OTHER = "other"


class ResolveReferenceErrorParsing(BaseModel):
    """
    Error parsing the secret reference
    """

    type: Literal[ResolveReferenceErrorTypes.PARSING] = (
        ResolveReferenceErrorTypes.PARSING
    )
    message: ErrorMessage


class ResolveReferenceErrorFieldNotFound(BaseModel):
    """
    The specified reference cannot be found within the item
    """

    type: Literal[ResolveReferenceErrorTypes.FIELD_NOT_FOUND] = (
        ResolveReferenceErrorTypes.FIELD_NOT_FOUND
    )


class ResolveReferenceErrorVaultNotFound(BaseModel):
    """
    No vault matched the secret reference query
    """

    type: Literal[ResolveReferenceErrorTypes.VAULT_NOT_FOUND] = (
        ResolveReferenceErrorTypes.VAULT_NOT_FOUND
    )


class ResolveReferenceErrorTooManyVaults(BaseModel):
    """
    More than one vault matched the secret reference query
    """

    type: Literal[ResolveReferenceErrorTypes.TOO_MANY_VAULTS] = (
        ResolveReferenceErrorTypes.TOO_MANY_VAULTS
    )


class ResolveReferenceErrorItemNotFound(BaseModel):
    """
    No item matched the secret reference query
    """

    type: Literal[ResolveReferenceErrorTypes.ITEM_NOT_FOUND] = (
        ResolveReferenceErrorTypes.ITEM_NOT_FOUND
    )


class ResolveReferenceErrorTooManyItems(BaseModel):
    """
    More than one item matched the secret reference query
    """

    type: Literal[ResolveReferenceErrorTypes.TOO_MANY_ITEMS] = (
        ResolveReferenceErrorTypes.TOO_MANY_ITEMS
    )


class ResolveReferenceErrorTooManyMatchingFields(BaseModel):
    """
    More than one field matched the provided secret reference
    """

    type: Literal[ResolveReferenceErrorTypes.TOO_MANY_MATCHING_FIELDS] = (
        ResolveReferenceErrorTypes.TOO_MANY_MATCHING_FIELDS
    )


class ResolveReferenceErrorNoMatchingSections(BaseModel):
    """
    No section found within the item for the provided identifier
    """

    type: Literal[ResolveReferenceErrorTypes.NO_MATCHING_SECTIONS] = (
        ResolveReferenceErrorTypes.NO_MATCHING_SECTIONS
    )


class ResolveReferenceErrorIncompatibleTOTPQueryParameterField(BaseModel):
    """
    Incompatiable TOTP query parameters
    """

    type: Literal[
        ResolveReferenceErrorTypes.INCOMPATIBLE_TOTP_QUERY_PARAMETER_FIELD
    ] = ResolveReferenceErrorTypes.INCOMPATIBLE_TOTP_QUERY_PARAMETER_FIELD


class ResolveReferenceErrorUnableToGenerateTotpCode(BaseModel):
    """
    The totp was not able to be generated
    """

    type: Literal[ResolveReferenceErrorTypes.UNABLE_TO_GENERATE_TOTP_CODE] = (
        ResolveReferenceErrorTypes.UNABLE_TO_GENERATE_TOTP_CODE
    )
    message: ErrorMessage


class ResolveReferenceErrorSSHKeyMetadataNotFound(BaseModel):
    """
    Couldn't find attributes specific to an SSH Key field
    """

    type: Literal[ResolveReferenceErrorTypes.S_SH_KEY_METADATA_NOT_FOUND] = (
        ResolveReferenceErrorTypes.S_SH_KEY_METADATA_NOT_FOUND
    )


class ResolveReferenceErrorUnsupportedFileFormat(BaseModel):
    """
    Currently only support text files
    """

    type: Literal[ResolveReferenceErrorTypes.UNSUPPORTED_FILE_FORMAT] = (
        ResolveReferenceErrorTypes.UNSUPPORTED_FILE_FORMAT
    )


class ResolveReferenceErrorIncompatibleSshKeyQueryParameterField(BaseModel):
    """
    Trying to convert a non-private key to a private key format
    """

    type: Literal[
        ResolveReferenceErrorTypes.INCOMPATIBLE_SSH_KEY_QUERY_PARAMETER_FIELD
    ] = ResolveReferenceErrorTypes.INCOMPATIBLE_SSH_KEY_QUERY_PARAMETER_FIELD


class ResolveReferenceErrorUnableToParsePrivateKey(BaseModel):
    """
    Unable to properly parse a private key string to convert to an internal Private Key type
    """

    type: Literal[ResolveReferenceErrorTypes.UNABLE_TO_PARSE_PRIVATE_KEY] = (
        ResolveReferenceErrorTypes.UNABLE_TO_PARSE_PRIVATE_KEY
    )


class ResolveReferenceErrorUnableToFormatPrivateKeyToOpenSsh(BaseModel):
    """
    Unable to format a private key to OpenSSH format
    """

    type: Literal[
        ResolveReferenceErrorTypes.UNABLE_TO_FORMAT_PRIVATE_KEY_TO_OPEN_SSH
    ] = ResolveReferenceErrorTypes.UNABLE_TO_FORMAT_PRIVATE_KEY_TO_OPEN_SSH


class ResolveReferenceErrorOther(BaseModel):
    """
    Other type
    """

    type: Literal[ResolveReferenceErrorTypes.OTHER] = ResolveReferenceErrorTypes.OTHER


ResolveReferenceError = Union[
    ResolveReferenceErrorParsing,
    ResolveReferenceErrorFieldNotFound,
    ResolveReferenceErrorVaultNotFound,
    ResolveReferenceErrorTooManyVaults,
    ResolveReferenceErrorItemNotFound,
    ResolveReferenceErrorTooManyItems,
    ResolveReferenceErrorTooManyMatchingFields,
    ResolveReferenceErrorNoMatchingSections,
    ResolveReferenceErrorIncompatibleTOTPQueryParameterField,
    ResolveReferenceErrorUnableToGenerateTotpCode,
    ResolveReferenceErrorSSHKeyMetadataNotFound,
    ResolveReferenceErrorUnsupportedFileFormat,
    ResolveReferenceErrorIncompatibleSshKeyQueryParameterField,
    ResolveReferenceErrorUnableToParsePrivateKey,
    ResolveReferenceErrorUnableToFormatPrivateKeyToOpenSsh,
    ResolveReferenceErrorOther,
]


class ResolveAllResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    individual_responses: Dict[
        str, Response[ResolvedReference, ResolveReferenceError]
    ] = Field(alias="individualResponses")


class SshKeyAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    public_key: str = Field(alias="publicKey")
    """
    The public part of the SSH Key
    """
    fingerprint: str
    """
    The fingerprint of the SSH Key
    """
    key_type: str = Field(alias="keyType")
    """
    The key type ("Ed25519" or "RSA, {length}-bit")
    """


class VaultOverview(BaseModel):
    """
    Represents a decrypted 1Password vault.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    """
    The vault's ID
    """
    title: str
    """
    The vault's title
    """
    created_at: Annotated[
        datetime,
        BeforeValidator(parse_rfc3339),
        PlainSerializer(serialize_datetime_data),
    ] = Field(alias="createdAt")
    """
    The time the vault was created at
    """
    updated_at: Annotated[
        datetime,
        BeforeValidator(parse_rfc3339),
        PlainSerializer(serialize_datetime_data),
    ] = Field(alias="updatedAt")
    """
    The time the vault was updated at
    """


class ItemListFilterByStateInner(BaseModel):
    """
    Generated type representing the anonymous struct variant `ByState` of the `ItemListFilter` Rust enum
    """

    active: bool
    archived: bool


class ItemListFilterTypes(str, Enum):
    BY_STATE = "ByState"


class ItemListFilterByState(BaseModel):
    type: Literal[ItemListFilterTypes.BY_STATE] = ItemListFilterTypes.BY_STATE
    content: ItemListFilterByStateInner


ItemListFilter = ItemListFilterByState


class PasswordRecipeMemorableInner(BaseModel):
    """
    Generated type representing the anonymous struct variant `Memorable` of the `PasswordRecipe` Rust enum
    """

    model_config = ConfigDict(populate_by_name=True)

    separator_type: SeparatorType = Field(alias="separatorType")
    """
    The type of separator between chunks.
    """
    capitalize: bool
    """
    Uppercase one randomly selected chunk.
    """
    word_list_type: WordListType = Field(alias="wordListType")
    """
    The type of word list used.
    """
    word_count: int = Field(alias="wordCount")
    """
    The number of "words" (words or syllables).
    """


class PasswordRecipePinInner(BaseModel):
    """
    Generated type representing the anonymous struct variant `Pin` of the `PasswordRecipe` Rust enum
    """

    length: int
    """
    Number of digits in the PIN.
    """


class PasswordRecipeRandomInner(BaseModel):
    """
    Generated type representing the anonymous struct variant `Random` of the `PasswordRecipe` Rust enum
    """

    model_config = ConfigDict(populate_by_name=True)

    include_digits: bool = Field(alias="includeDigits")
    """
    Include at least one digit in the password.
    """
    include_symbols: bool = Field(alias="includeSymbols")
    """
    Include at least one symbol in the password.
    """
    length: int
    """
    The length of the password.
    """


class PasswordRecipeTypes(str, Enum):
    MEMORABLE = "Memorable"
    PIN = "Pin"
    RANDOM = "Random"


class PasswordRecipeMemorable(BaseModel):
    type: Literal[PasswordRecipeTypes.MEMORABLE] = PasswordRecipeTypes.MEMORABLE
    parameters: PasswordRecipeMemorableInner


class PasswordRecipePin(BaseModel):
    type: Literal[PasswordRecipeTypes.PIN] = PasswordRecipeTypes.PIN
    parameters: PasswordRecipePinInner


class PasswordRecipeRandom(BaseModel):
    type: Literal[PasswordRecipeTypes.RANDOM] = PasswordRecipeTypes.RANDOM
    parameters: PasswordRecipeRandomInner


PasswordRecipe = Union[PasswordRecipeMemorable, PasswordRecipePin, PasswordRecipeRandom]


class SeparatorType(str, Enum):
    DIGITS = "digits"
    """
    Randomly selected digits.
    E.g, "`correct4horse0battery1staple`"
    """
    DIGITSANDSYMBOLS = "digitsAndSymbols"
    """
    Randomly selected digits and symbols.
    This is useful to get word-based passwords to meet complexity requirements
    E.g, "`correct4horse-battery1staple`"
    """
    SPACES = "spaces"
    """
    Spaces, like the original Diceware.
    Great for mobile keyboards, not so great when people can overhear you type the password.
    E.g, "`correct horse battery staple`"
    """
    HYPHENS = "hyphens"
    """
    Hyphens "`-`".
    E.g, "`correct-horse-battery-staple`"
    """
    UNDERSCORES = "underscores"
    """
    "`_`".
    E.g, "`correct_horse_battery_staple`"
    """
    PERIODS = "periods"
    """
    Period (full stop) "`.`".
    E.g, "`correct.horse.battery.staple`"
    """
    COMMAS = "commas"
    """
    Comma "`,`".
    E.g, "`correct,horse,battery,staple`"
    """


class WordListType(str, Enum):
    FULLWORDS = "fullWords"
    """
    Agile wordlist
    """
    SYLLABLES = "syllables"
    """
    English-like syllables
    """
    THREELETTERS = "threeLetters"
    """
    Three (random) letter "words"
    """
